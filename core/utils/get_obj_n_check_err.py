from typing       import Tuple, Any

from users.models import User
from raids.models import RaidHistory


class GetRaidHistory:
    
    def get_raid_n_check_error(raid_history_id: int, user: User) -> Tuple[Any, str]:
        try:
            raid = RaidHistory.objects\
                              .get(id=raid_history_id)
        except RaidHistory.DoesNotExist:
            return None, f'보스레이드 {raid_history_id}(id)는 존재하지 않습니다.'
        
        if not user.nickname == raid.users.nickname:
            return None, f'다른 유저의 보스레이드입니다.'
        
        return raid, None