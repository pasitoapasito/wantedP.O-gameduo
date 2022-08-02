from django.urls import path

from users.views.user_signup  import UserSignUpView
from users.views.user_signin  import UserSignInView
from users.views.user_signout import UserSignOutView

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
    path('/signout', UserSignOutView.as_view()),
]

urlpatterns += [
    path('/token/refresh', TokenRefreshView.as_view()),
]