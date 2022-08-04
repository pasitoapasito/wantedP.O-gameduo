from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.utils.check_obj_status import GetRaid
from core.utils.redis_cache      import RedisCache
from raids.serializers           import BossRaidStatusSerializer, BossRaidStatusSchema


class BossRaidStatusView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(responses={200: BossRaidStatusSchema})
    def get(self, request):
        
        RedisCache.set_raid_data_in_cache()
        
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