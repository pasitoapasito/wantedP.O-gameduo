from rest_framework.views       import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response    import Response

from drf_yasg       import openapi
from drf_yasg.utils import swagger_auto_schema

from core.utils.decorator           import query_debugger
from core.utils.get_obj_n_check_err import GetUserHistory

from users.serializers import UserSearchSerializer, UserSearchSchema


class UserSearchView(APIView):
    """
    Assignee: 김동규
    
    query param: nickname
    query string: offset, limit
    return: json
    detail:
      - 인증/인가에 통과한 유저는 특정 유저의 정보를 조회할 수 있습니다. (GET: 보스레이드 유저조회 기능)
        > 유저정보 조회
          * 특정 유저의 보스레이드 총점 정보를 반환함
          * 특정 유저의 보스레이드 히스토리 내역을 반환함(default: 10개)
          * 존재하지 않는 유저의 정보는 조회할 수 없습니다.
    """
    
    permission_classes = [IsAuthenticated]
    
    offset   = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit    = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    nickname = openapi.Parameter('nickname', openapi.IN_PATH, required=True, type=openapi.TYPE_STRING)
    
    @query_debugger
    @swagger_auto_schema(responses={200: UserSearchSchema}, manual_parameters=[nickname, offset, limit])
    def get(self, request, nickname):
        """
        유저정보 조회 데이터 개수 선택
        """
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))
        
        """
        유저 객제정보 확인
        """
        histories, user, err = GetUserHistory.get_user_history_n_check_error(nickname, offset, limit)
        if err:
            return Response({'detail': err}, status=400)
        
        """
        반환 데이터
          - 유저 닉네임
          - 유저 보스레이드 총점
          - 유저 히스토리 내역
        """
        data = {
            'nickname'   : user.nickname,
            'total_score': sum([raid.score for raid in histories]),
            'histories'  : UserSearchSerializer(histories, many=True).data
        }
        
        return Response(data, status=200)