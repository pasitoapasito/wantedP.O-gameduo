from django.urls import path

from raids.views.raid_enter  import BossRaidEnterView
from raids.views.raid_end    import BossRaidEndView
from raids.views.raid_status import BossRaidStatusView


urlpatterns = [
    path('/enter', BossRaidEnterView.as_view()),
    path('/status', BossRaidStatusView.as_view()),
    path('/<int:raid_history_id>/end', BossRaidEndView.as_view()),
]