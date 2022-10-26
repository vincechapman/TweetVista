from django.urls import path

from TLAPIWebTest.auth.views import LoginView
from TLAPIWebTest.client.views import LandingPage

urlpatterns = [
    path('landing_page/', LandingPage.as_view(), name='client-landing'),
]
