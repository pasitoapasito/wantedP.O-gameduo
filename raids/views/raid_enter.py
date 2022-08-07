import json

from rest_framework.views        import APIView
from rest_framework.response     import Response
from rest_framework.permissions  import IsAuthenticated

from core.utils.check_obj_status import GetRaid, RaidTime
from core.utils.redis_queue      import RedisQueue
from core.utils.redis_cache      import RedisCache

from drf_yasg.utils    import swagger_auto_schema
from raids.serializers import BossRaidEnterSerializer


class BossRaidEnterView(APIView):
    """
    Assignee: 김동규
    
    request body: level(필수값)
    return: json
    detail:
      - 인증/인가에 통과한 유저는 보스레이드를 시작할 수 있습니다. (POST: 보스레이드 입장 기능)
        > 보스레이드 입장조건
          * 보스레이드 입장 요청이 들어오면 캐싱정보를 초기화합니다.
          * 보스레이드 입장은 1명만 가능합니다.
          * 동시성 문제를 해결하기 위해 Redis queue를 활용하여 유저 대기열을 만들었습니다.
          * 이미 보스레이드가 진행 중이라면 보스레이드에 입장할 수 없습니다. (상태코드 202 반환)
          * 보스레이드가 시작되면 제한시간 내에 클리어를 해야합니다.
          * 제한시간 내에 클리어하지 못할 경우, 강제로 자동 실패처리 됩니다. (background task)
          * 보스레이드의 (캐싱)정보가 존재하지 않으면 에러를 반환합니다.
          * 보스레이드 입장이 성공적으로 이루어지면, 유저 대기열 및 보스레이드 정보를 모두 삭제합니다.
    """
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=BossRaidEnterSerializer, responses={201: BossRaidEnterSerializer})
    def post(self, request):
        """
        POST: 보스레이드 입장(시작) 기능
        """
        user = request.user
        
        """
        보스레이드 정보를 Redis에 캐싱(저장)
        """
        RedisCache.set_raid_data_in_cache()
        
        """
        현재 진행중인 보스레이드의 존재여부 확인
        """
        raid, err = GetRaid.get_raid_in_progress()
        if err:
            return Response({'detail': err}, status=400)
        if raid:
            return Response(
                {
                    'msg': '이미 진행중인 보스레이드가 있습니다.', 'is_entered': False,\
                    'raid_history_id': raid[0].id
                },
                status=202
            )
        
        """
        동시성 문제를 해결하기 위해 Redis queue를 활용했습니다.
        단, 배포 시 RedisQueue의 host를 변경해야 합니다.
        """
        queue = RedisQueue('queue', host='localhost', port=6379, db=2)
        
        """
        유저 대기열(queue)을 만들고, 대기열의 맨 앞에 있는 유저를 보스레이드에 입장시킵니다.
        """
        queue.put(json.dumps({'user_queue': user.id}))
        element = json.loads(queue.get())
        
        if not user.id == element['user_queue']:
            queue.clear()
            return Response({'msg': '다른 유저가 이미 보스레이드에 입장했습니다.', 'is_entered': False}, status=202)
        
        """
        모든 유효성 검사 통과후, 보스레이드 히스토리 생성
        """
        serializer = BossRaidEnterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(users=user)
            """
            보스레이드의 제한시간을 초과하면 강제로 보스레이드를 종료하는 백그라운드 태스크 생성
            """
            RaidTime.check_raid_time(serializer.data['id'])
            """
            보스레이드 입장 후 모든 보스레이드 캐싱정보를 삭제함(유저 대기열 포함)
            """
            queue.clear()
            return Response({'msg': '보스레이드에 입장했습니다.', 'is_entered': True, 'result': serializer.data}, status=201)
        """
        유효성 검사에 실패하면 보스레이드 입장을 제한하고 보스레이드의 모든 캐싱정보 삭제
        """
        queue.clear()
        return Response(serializer.errors, status=400)