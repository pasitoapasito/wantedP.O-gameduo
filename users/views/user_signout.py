from rest_framework.views            import APIView
from rest_framework.permissions      import IsAuthenticated
from rest_framework.response         import Response
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken, RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg       import openapi


class UserSignOutView(APIView):
    """
    Assignee: 김동규
    
    request body: refresh token
    return: json
    detail: 유저 로그아웃 기능입니다.
    """
    
    permission_classes = [IsAuthenticated]
    
    post_params = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'refesh_token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    )
    @swagger_auto_schema(request_body=post_params, responses={200: '유저가 로그아웃 되었습니다.'})
    def post(self, request):
        """
        POST: 유저 로그아웃 기능
        """
        user = request.user
        
        """
        입력한 리프레시 토큰의 정보를 가져옵니다.
        """
        try:
            refresh = RefreshToken(request.data['refesh_token'])
        except:
            return Response({'detail': '유효하지 않거나 만료된 토큰입니다.'}, status=400)
        
        """
        입력한 리프레시 토큰이 본인(API 요청자)의 토큰인지를 확인합니다.
        """
        if not user.id == refresh['user_id']:
            return Response({'detail': '유저의 토큰정보가 유효하지 않습니다.'}, status=400)
        
        """
        해당 유저의 발급된 모든 리프레시 토큰을 사용 제한합니다.
        """
        for token in OutstandingToken.objects.filter(user_id=refresh['user_id']):
            BlacklistedToken.objects.get_or_create(token=token)
            
        return Response({'message' : f'유저 {user.nickname}이 로그아웃 되었습니다.'}, status=200)