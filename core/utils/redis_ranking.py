from typing import Tuple, Any

from django.db.models  import Sum, F
from django.core.cache import cache

from raids.models import RaidHistory
from users.models import User


class RedisRanking:
    
    def set_n_get_top_10_redis_ranking() -> Tuple[Any, str]:
        histories = RaidHistory.objects\
                               .values('users')\
                               .annotate(total_score=Sum('score'), nickname=F('users__nickname'))[0:10]
                               
        data = sorted(histories, key=(lambda x: x['total_score']), reverse=True)
        
        ranking_list = []
        """
        - TODO: 동점자 랭킹순위 조정
        """
        for idx, rank in enumerate(data):
            if rank['total_score'] > 0:
                rank['ranking'] = idx
            else:
                rank['ranking'] = None
                
            ranking_list.append(rank)
            
        cache.set('ranking', ranking_list, timeout=None)
        
        ranking = cache.get('ranking')
        if not ranking:
            return None, '보스레이드의 정보를 찾지 못했습니다.'
        
        return ranking, None
            

class GetMyRanking:
    
    def get_my_ranking(ranking_list: list, user: User) -> Tuple[Any, str]:
        result = list(filter(lambda x: x['nickname'] == user.nickname, ranking_list))
        
        if not result or\
           result[0]['ranking'] is None:
               return None, f'{user.nickname}님을 랭킹 TOP10 순위에서 찾을 수 없습니다.'
        
        return result[0], None