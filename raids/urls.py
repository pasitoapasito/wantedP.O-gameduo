from django.urls import path

from raids.views.raid_enter   import BossRaidEnterView
from raids.views.raid_end     import BossRaidEndView
from raids.views.raid_status  import BossRaidStatusView
from raids.views.raid_ranking import BossRaidRankingView


"""
보스레이드 입장/종료/상태조회/랭킹조회 url patterns
"""
urlpatterns = [
    path('/enter', BossRaidEnterView.as_view()),
    path('/status', BossRaidStatusView.as_view()),
    path('/<int:raid_history_id>/end', BossRaidEndView.as_view()),
    path('/ranking', BossRaidRankingView.as_view()),
]