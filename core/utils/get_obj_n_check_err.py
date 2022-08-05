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
    

class GetUserHistory:
    
    def get_user_history_n_check_error(nickname: str, offset: int, limit: int) -> Tuple[Any, Any, str]:
        try:
            user = User.objects\
                       .get(nickname=nickname)
        except User.DoesNotExist:
            return None, None, f'유저 {nickname}는 존재하지 않습니다.'
        
        histories = RaidHistory.objects\
                               .filter(users=user)\
                               .order_by('-enter_time')[offset:offset+limit]
        
        return histories, user, None     