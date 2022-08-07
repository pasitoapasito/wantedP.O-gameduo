from typing       import Tuple, Any

from users.models import User
from raids.models import RaidHistory


class GetRaidHistory:
    """
    Assignee: 김동규
    
    param: raid_history_id, user
    return: obj, err
    detail:
      - 보스레이드 id를 통해 보스레이드 객체(정보)의 존재여부 확인
      - 보스레이드 객체의 유저정보와 API를 호출한 유저의 정보를 대조
    """
    
    def get_raid_n_check_error(raid_history_id: int, user: User) -> Tuple[Any, str]:
        """
        보스레이드 객체/에러 확인
        """
        try:
            raid = RaidHistory.objects\
                              .get(id=raid_history_id)
        except RaidHistory.DoesNotExist:
            return None, f'보스레이드 {raid_history_id}(id)는 존재하지 않습니다.'
        
        if not user.nickname == raid.users.nickname:
            return None, f'다른 유저의 보스레이드입니다.'
        
        return raid, None
    

class GetUserHistory:
    """
    Assignee: 김동규
    
    param: nickname, offset, limit
    return: obj(raid histories), obj(user), err
    detail:
      - nickname을 통해 유저 객체(정보)의 존재여부 확인
      - offset, limit 설정만큼 보스레이드 히스토리 내역을 반환함
      - 보스레이드 히스토리 내역은 최신순으로 정렬하여 반환함
    """
    
    def get_user_history_n_check_error(nickname: str, offset: int, limit: int) -> Tuple[Any, Any, str]:
        """
        유저 객체/에러 확인 및 유저 히스토리 조회 
        """
        try:
            user = User.objects\
                       .get(nickname=nickname)
        except User.DoesNotExist:
            return None, None, f'유저 {nickname}는 존재하지 않습니다.'
        
        histories = RaidHistory.objects\
                               .filter(users=user)\
                               .order_by('-enter_time')[offset:offset+limit]
        
        return histories, user, None     