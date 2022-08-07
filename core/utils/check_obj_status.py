from typing   import Tuple, Any
from datetime import datetime, timedelta

from django.core.cache import cache
from background_task   import background
from raids.models      import RaidHistory


class GetRaid:
    """
    Assignee: 김동규
    
    return: obj, err
    detail:
      - 현재 진행중인 보스레이드의 존재여부 확인
      - Redis의 캐싱정보를 활용하여 보스레이드 진행여부 판단(제한시간)
    """
    
    def get_raid_in_progress() -> Tuple[Any, str]:
        history = RaidHistory.objects\
                             .filter(status='in_progress', end_time=None)
        
        now        = datetime.now()
        limit_time = cache.get('limit_time')
        
        if not limit_time:
            return None, '보스레이드의 정보를 찾지 못했습니다.'
        
        """
        입장 시점으로부터 제한시간을 초과하지 않은 보스레이드를 필터링함(현재 진행중인 보스레이드)
        """
        raid = history.filter(
            enter_time__gte=now-timedelta(seconds=int(limit_time))
        )
        return raid, None
    
    
class RaidTime:
    """
    Assignee: 김동규
    
    print: 보스레이드 강제종료 안내
    detail:
      - 보스레이드의 제한시간을 초과하면 보스레이드를 강제 종료함(score: 0)
      - 보스레이드 히스토리의 status를 실패로 변경하고, end time을 제한시간 초과시점으로 적용
    """
    
    TIME = int(cache.get('limit_time'))
    
    @background(schedule=TIME)
    def check_raid_time(RAID: int):
        raid = RaidHistory.objects\
                          .get(id=RAID)
        
        raid.status   = 'fail'
        raid.end_time = datetime.now()
        raid.save()
        
        print(f'보스레이드 {raid.id}(id)를 제한시간 내에 클리어하지 못했습니다.')