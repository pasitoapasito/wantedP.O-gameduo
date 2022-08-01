from rest_framework.views            import APIView
from rest_framework.permissions      import IsAuthenticated
from rest_framework.response         import Response
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken, RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg       import openapi


class UserSignOutView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    post_params = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'refesh_token': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    )
    @swagger_auto_schema(request_body=post_params, responses={200: '유저가 로그아웃 되었습니다.'})
    def post(self, request):
        user = request.user
        
        try:
            refresh = RefreshToken(request.data['refesh_token'])
        except:
            return Response({'detail': '유효하지 않거나 만료된 토큰입니다.'}, status=400)
        
        for token in OutstandingToken.objects.filter(user_id=refresh['user_id']):
            BlacklistedToken.objects.get_or_create(token=token)
            
        return Response({'message' : f'유저 {user.nickname}이 로그아웃 되었습니다.'}, status=200)