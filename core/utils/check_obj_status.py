from typing   import Tuple, Any
from datetime import datetime, timedelta

from django.core.cache import cache
from background_task   import background
from raids.models      import RaidHistory


class GetRaid:
    
    def get_raid_in_progress() -> Tuple[Any, str]:
        history = RaidHistory.objects\
                             .filter(status='in_progress', end_time=None)
        
        now        = datetime.now()
        limit_time = cache.get('limit_time')
        
        if not limit_time:
            return None, '보스레이드의 정보를 찾지 못했습니다.'
        
        raid = history.filter(
            enter_time__gte=now-timedelta(seconds=int(limit_time))
        )
        return raid, None
    
    
class RaidTime:
    
    TIME = int(cache.get('limit_time'))
    
    @background(schedule=TIME)
    def check_raid_time(RAID: int):
        raid = RaidHistory.objects\
                          .get(id=RAID)
        
        raid.status   = 'fail'
        raid.end_time = datetime.now()
        raid.save()
        
        print(f'보스레이드 {raid.id}(id)를 제한시간 내에 클리어하지 못했습니다.')