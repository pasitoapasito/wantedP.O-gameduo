from django.urls import path

from users.views.user_signup import UserSignUpView
from users.views.user_signin import UserSignInView


urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view()),
]