from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.utils.redis_ranking import RedisRanking, GetMyRanking


class BossRaidRankingView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(responses={200: '보스레이드 랭킹 TOP10 조회에 성공했습니다.'})
    def get(self, request):
        user = request.user
        
        ranking_list, err = RedisRanking.set_n_get_top_10_redis_ranking()
        if err:
            return Response({'detail': err}, status=400)
        
        my_data, info = GetMyRanking.get_my_ranking(ranking_list, user)
        if my_data:
            my_ranking = my_data
        if info:
            my_ranking = {
                'users': user.id, 'total_score': '랭킹 순위권에 존재하지 않는 점수입니다.',\
                'ranking': info, 'nickname': user.nickname
            }

        total_data = {
            'top_10_ranker': ranking_list,
            'my_ranking'   : my_ranking
        }
        
        return Response(total_data, status=200)