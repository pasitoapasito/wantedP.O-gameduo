from typing import Tuple, Any

from django.db.models  import Sum, F
from django.core.cache import cache

from raids.models import RaidHistory
from users.models import User


class RedisRanking:
    """
    Assignee: 김동규
    
    return: obj, err
    detail:
      - 유저 정보와 보스레이드 총 점수를 계산
      - 총 점수를 기준으로 보스레이드 랭킹을 산출함(TOP10)
      - 보스레이드 랭킹정보를 Redis cache에 저장(캐싱) 후 가져옴
    """
    
    def set_n_get_top_10_redis_ranking() -> Tuple[Any, str]:
        """
        유저별 보스레이드 총 점수 계산(랭킹 TOP10)
        """
        histories = RaidHistory.objects\
                               .values('users')\
                               .annotate(total_score=Sum('score'), nickname=F('users__nickname'))[0:10]
        
        """
        총 점수(높은순)을 기준으로 정렬
        """                       
        data = sorted(histories, key=(lambda x: x['total_score']), reverse=True)
        
        ranking_list = []
        """
        보스레이드 랭킹 산출
          - 랭킹 순위권에 기록이 존재하더라도 score가 0점이면 ranking은 Null값으로 지정
          - TODO: 동점자 랭킹순위 조정
        """
        for idx, rank in enumerate(data):
            if rank['total_score'] > 0:
                rank['ranking'] = idx
            else:
                rank['ranking'] = None
                
            ranking_list.append(rank)
        
        """
        보스레이드 랭킹정보 캐싱(저장)
        """    
        cache.set('ranking', ranking_list, timeout=None)
        
        """
        보스레이드 랭킹(캐싱)정보 참조
        """
        ranking = cache.get('ranking')
        if not ranking:
            return None, '보스레이드의 정보를 찾지 못했습니다.'
        
        return ranking, None
            

class GetMyRanking:
    """
    Assignee: 김동규
    
    param: ranking list, user
    return: obj, info
    detail:
      - 보스레이드 TOP10 랭킹정보에서 본인의 기록이 존재하는지 확인
      - 만약, 존재하지 않을 경우 본인의 기록이 순위권 밖이라는 메세지 반환(info)
    """
    
    def get_my_ranking(ranking_list: list, user: User) -> Tuple[Any, str]:
        """
        TOP10 랭킹정보에서 본인의 기록을 조회
        """
        result = list(filter(lambda x: x['nickname'] == user.nickname, ranking_list))
        
        """
        순위권에 기록이 없는 경우 or 순위권에 기록이 있더라도 score가 0점인 경우
        """
        if not result or\
           result[0]['ranking'] is None:
               return None, f'{user.nickname}님을 랭킹 TOP10 순위에서 찾을 수 없습니다.'
        
        return result[0], None