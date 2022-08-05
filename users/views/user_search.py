from rest_framework.views       import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response    import Response

from drf_yasg       import openapi
from drf_yasg.utils import swagger_auto_schema

from core.utils.decorator           import query_debugger
from core.utils.get_obj_n_check_err import GetUserHistory

from users.serializers import UserSearchSerializer, UserSearchSchema


class UserSearchView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    offset   = openapi.Parameter('offset', openapi.IN_QUERY, required=False, pattern='?offset=', type=openapi.TYPE_STRING)
    limit    = openapi.Parameter('limit', openapi.IN_QUERY, required=False, pattern='?limit=', type=openapi.TYPE_STRING)
    nickname = openapi.Parameter('nickname', openapi.IN_PATH, required=True, type=openapi.TYPE_STRING)
    
    @query_debugger
    @swagger_auto_schema(responses={200: UserSearchSchema}, manual_parameters=[nickname, offset, limit])
    def get(self, request, nickname):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 10))
        
        histories, user, err = GetUserHistory.get_user_history_n_check_error(nickname, offset, limit)
        if err:
            return Response({'detail': err}, status=400)
        
        data = {
            'nickname'   : user.nickname,
            'total_score': sum([raid.score for raid in histories]),
            'histories'  : UserSearchSerializer(histories, many=True).data
        }
        
        return Response(data, status=200)