from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView

from TLAPIWebTest.auth.mixins.login import LoginMixin
from TLAPIWebTest.auth.mixins.messaging import MessageMixin

class LandingPage(LoginMixin, MessageMixin, TemplateView):
    template_name = 'client/landing_page.html'



