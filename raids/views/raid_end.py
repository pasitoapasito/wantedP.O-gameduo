from rest_framework.views           import APIView
from rest_framework.response        import Response
from rest_framework.permissions     import IsAuthenticated

from core.utils.get_obj_n_check_err import GetRaidHistory
from core.utils.redis_cache         import RedisCache

from drf_yasg          import openapi
from drf_yasg.utils    import swagger_auto_schema
from raids.serializers import BossRaidEndSerializer


class BossRaidEndView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    raid_id = openapi.Parameter('raid_history_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(
        request_body=BossRaidEndSerializer, responses={200: BossRaidEndSerializer},\
        manual_parameters=[raid_id]
    )
    def patch(self, request, raid_history_id):
        user = request.user
        
        RedisCache.set_raid_data_in_cache()
        
        raid, err = GetRaidHistory.get_raid_n_check_error(raid_history_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = BossRaidEndSerializer(raid, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '보스레이드를 성공적으로 클리어했습니다.', 'result': serializer.data}, status=200)
        return Response(serializer.errors, status=400)