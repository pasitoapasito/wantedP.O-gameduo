from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.utils.check_obj_status import GetRaid
from core.utils.redis_cache      import RedisCache
from core.utils.decorator        import query_debugger

from raids.serializers import BossRaidStatusSerializer, BossRaidStatusSchema


class BossRaidStatusView(APIView):
    """
    Assignee: 김동규
    
    return: json
    detail:
      - 인증/인가에 통과한 유저는 보스레이드의 상태정보를 조회할 수 있습니다. (GET: 보스레이드 상태조회 기능)
        > 보스레이드 상태조회
          * 이미 진행중인 보스레이드가 있으면, 보스레이드에 입장한 유저정보(id)와 입장불가 정보(can enter: False)를 함께 반환함
          * 현재 진행중인 보스레이드가 없다면, 보스레이드에 입장한 유저정보(null)와 입장가능 정보(can enter: True)를 함께 반환함
          * 보스레이드의 (캐싱)정보가 존재하지 않으면 에러를 반환합니다.
    """
    
    permission_classes = [IsAuthenticated]
    
    @query_debugger
    @swagger_auto_schema(responses={200: BossRaidStatusSchema})
    def get(self, request):
        """
        GET: 보스레이드 상태조회 기능
        """
        
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
            serializer = BossRaidStatusSerializer(raid, many=True)
            return Response(
                {
                    'msg': '이미 진행중인 보스레이드가 있습니다.', 'can_enter': False,\
                    'entered_user_id': serializer.data[0]['user_id']
                },
                status=200
            )
        return Response(
            {
                'msg': '현재 진행중인 보스레이드가 없습니다.', 'can_enter': True,\
                'entered_user_id': None
            },
            status=200
        )