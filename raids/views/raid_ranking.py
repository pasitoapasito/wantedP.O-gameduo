from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.utils.redis_ranking import RedisRanking, GetMyRanking
from core.utils.decorator     import query_debugger


class BossRaidRankingView(APIView):
    """
    Assignee: 김동규
    
    return: json
    detail:
      - 인증/인가에 통과한 유저는 보스레이드의 TOP10 랭킹을 조회할 수 있습니다. (GET: 보스레이드 랭킹조회 기능)
        > 보스레이드 랭킹조회
          * 보스레이드의 상위권 TOP10의 랭킹정보를 조회합니다.
          * API 요청자의 기록이 해당 순위권에 존재하는지 확인합니다.
          * 만약 존재할 경우 랭킹정보와 본인의 기록을 함께 반환합니다.
          * 만약 존재하지 않을 경우 랭킹정보와 본인의 기록이 순위권 밖이라는 메세지를 함께 반환합니다.
          * 보스레이드의 (캐싱)정보가 존재하지 않으면 에러를 반환합니다.
    """
    
    permission_classes = [IsAuthenticated]
    
    @query_debugger
    @swagger_auto_schema(responses={200: '보스레이드 랭킹 TOP10 조회에 성공했습니다.'})
    def get(self, request):
        """
        GET: 보스레이드 랭킹조회 기능
        """
        user = request.user
        
        """
        보스레이드 랭킹정보 캐싱(저장)/추출
        """
        ranking_list, err = RedisRanking.set_n_get_top_10_redis_ranking()
        if err:
            return Response({'detail': err}, status=400)
        
        """
        본인의 랭킹정보 조회
          - 랭킹 순위권(TOP10)에 본인의 기록이 포함되는지 확인
          - 포함된다면 해당 기록을 랭킹 데이터와 함께 반환, 포함되지 않는다면 순위권 밖이라는 메세지 반환
        """
        my_data, info = GetMyRanking.get_my_ranking(ranking_list, user)
        if my_data:
            my_ranking = my_data
        if info:
            my_ranking = {
                'users': user.id, 'total_score': '랭킹 순위권에 존재하지 않는 점수입니다.',\
                'ranking': info, 'nickname': user.nickname
            }
        
        """
        최종 반환 데이터
          - 보스레이드 TOP10 랭킹순위 정보
          - API 요청자의 랭킹순위 정보
        """
        total_data = {
            'top_10_ranker': ranking_list,
            'my_ranking'   : my_ranking
        }
        
        return Response(total_data, status=200)