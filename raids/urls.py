from django.urls import path

from raids.views.raid_enter import BossRaidEnterView


urlpatterns = [
    path('/enter', BossRaidEnterView.as_view()),
]
