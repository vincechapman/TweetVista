from django.urls import path

from TLAPIWebTest.auth.views import LoginView, UserLogout, AuthTwitterAc

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('auth_twitter/', AuthTwitterAc.as_view(), name='auth-twitter-account'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
]
