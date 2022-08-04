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
    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=BossRaidEnterSerializer, responses={201: BossRaidEnterSerializer})
    def post(self, request):
        user = request.user
        
        RedisCache.set_raid_data_in_cache()
        
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
        
        queue.put(json.dumps({'user_queue': user.id}))
        element = json.loads(queue.get())
        
        if not user.id == element['user_queue']:
            queue.clear()
            return Response({'msg': '다른 유저가 이미 보스레이드에 입장했습니다.', 'is_entered': False}, status=202)
        
        serializer = BossRaidEnterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(users=user)
            RaidTime.check_raid_time(serializer.data['id'])
            queue.clear()
            return Response({'msg': '보스레이드에 입장했습니다.', 'is_entered': True, 'result': serializer.data}, status=201)
        queue.clear()
        return Response(serializer.errors, status=400)