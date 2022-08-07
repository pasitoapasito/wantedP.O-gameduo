from rest_framework.views           import APIView
from rest_framework.response        import Response
from rest_framework.permissions     import IsAuthenticated

from core.utils.get_obj_n_check_err import GetRaidHistory
from core.utils.redis_cache         import RedisCache

from drf_yasg          import openapi
from drf_yasg.utils    import swagger_auto_schema
from raids.serializers import BossRaidEndSerializer


class BossRaidEndView(APIView):
    """
    Assignee: 김동규
    
    query param: raid_history_id
    request body: level(필수값)
    return: json
    detail:
      - 인증/인가에 통과한 유저는 보스레이드를 종료할 수 있습니다. (PATCH: 보스레이드 종료 기능)
        > 보스레이드 종료조건
          * 보스레이드 종료 요청이 들어오면 캐싱정보를 초기화합니다.
          * 본인의 보스레이드만 종료할 수 있습니다.
          * 현재 진행중인 보스레이드만 종료할 수 있습니다. (제한시간을 초과한 보스레이드는 종료 불가능)
          * 존재하지 않는 보스레이드는 종료할 수 없습니다.
          * 보스레이드를 성공적으로 종료하면, 보스레이드 강제종료 백그라운드 태스크(TASK)도 함께 삭제합니다.
    """
    
    permission_classes = [IsAuthenticated]
    
    raid_id = openapi.Parameter('raid_history_id', openapi.IN_PATH, required=True, type=openapi.TYPE_INTEGER)
    
    @swagger_auto_schema(
        request_body=BossRaidEndSerializer, responses={200: BossRaidEndSerializer},\
        manual_parameters=[raid_id]
    )
    def patch(self, request, raid_history_id):
        """
        PATCH: 보스레이드 종료 기능
        """
        user = request.user
        
        """
        보스레이드 정보를 Redis에 캐싱(저장)
        """
        RedisCache.set_raid_data_in_cache()
        
        """
        보스레이드 객체/유저정보 확인
        """
        raid, err = GetRaidHistory.get_raid_n_check_error(raid_history_id, user)
        if err:
            return Response({'detail': err}, status=400)
        
        serializer = BossRaidEndSerializer(raid, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '보스레이드를 성공적으로 클리어했습니다.', 'result': serializer.data}, status=200)
        return Response(serializer.errors, status=400)