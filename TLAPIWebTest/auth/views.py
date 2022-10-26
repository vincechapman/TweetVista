# from django.conf import settings
# from django.contrib.auth import logout
from django.http import HttpResponseRedirect
# from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView

from TLAPIWebTest.auth.forms import LoginForm
from TLAPIWebTest.auth.mixins.login import LoginMixin
from TLAPIWebTest.auth.mixins.messaging import MessageMixin
from TLAPIWebTest.auth.utils import construct_twitter_callback, twitter_get_oauth_request_token, twitter_get_oauth_token, \
    twitter_get_access_tokens, verify_twitter_credentials
from TLAPIWebTest.tlapi.web.webconn_singleton import WebConnection


class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    # Create your views here.

    def get_form(self, form_class=LoginForm):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs['class'] = 'form-control'
        form.fields['username'].widget.attrs['placeholder'] = 'User Name'
        form.fields['password'].widget.attrs['class'] = 'form-control'
        form.fields['password'].widget.attrs['placeholder'] = 'Password'
        form.request = self.request
        return form

    def get_success_url(self):
        next_var = self.request.GET.get('next', '')
        return next_var


class AuthTwitterAc(LoginMixin, MessageMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        wc = WebConnection()
        data = wc.get_twitter_app()
        if data['status'] != 200:
            self.error(f'{data["msg"]} - status:{data["status"]}', request)
            return HttpResponseRedirect(reverse('client-landing'))
        self.info(f'{data["msg"]} - status:{data["status"]}', request)
        ck = data['data']['consumer_key']
        cs = data['data']['consumer_secret']
        callback = data['data']['callback']
        callback = construct_twitter_callback(callback, request)
        ro_key, ro_secret = twitter_get_oauth_request_token(cs, ck, callback)
        if ro_key is None and ro_secret is None:
            self.error('AuthoriseView.get: Cannot get auth request tokens')
            return HttpResponseRedirect(reverse('client-landing'))
        twitter_app = {
            'app_name': data['data']['name'],
            'consumer_key': ck,
            'consumer_secret': cs,
            'resource_owner_key': ro_key,
            'resource_owner_secret': ro_secret
        }
        request.session['twitter_app'] = twitter_app
        url = 'https://api.twitter.com/oauth/authorize?oauth_token=' + ro_key + '&force_login=true'
        return HttpResponseRedirect(url)


class TwitterLoginCallback(LoginMixin, MessageMixin, View):
    def get(self, request, *args, **kwargs):  # TODO Consider removing args and kwargs as not being used
        oauth_token = request.GET.get('oauth_token', None)
        oauth_verifier = request.GET.get('oauth_verifier', None)
        twitter_app = request.session.pop('twitter_app', None)
        if twitter_app is None:
            self.error('TwitterLoginCallback.get: Cannot get twitter app data from session')
            return reverse('client-landing')
        access_token_list = twitter_get_oauth_token(oauth_verifier, twitter_app)
        access_tokens = twitter_get_access_tokens(access_token_list, twitter_app)
        only_tokens = {i: access_tokens[i] for i in access_tokens}
        only_tokens['user_data'] = verify_twitter_credentials(access_tokens)
        only_tokens['app_name'] = request.session.pop('twitter_appname', None)
        only_tokens['app_name'] = twitter_app.get('app_name', None)
        only_tokens['target_id'] = request.session.pop('twitter_target_id', None)

        wc = WebConnection()
        msg = wc.store_user_twitter_account(only_tokens)
        self.info(f"{only_tokens['app_name']} authorised {only_tokens['handle']}")
        return HttpResponseRedirect(reverse('client-landing'))


class UserLogout(LoginMixin, View):

    def get(self, request, *args, **kwargs):

        sessionid = request.session.get('tlapi_session_id',None)
        if sessionid is not None:
            wc = WebConnection()
            ret_dict=wc.logout()
            pass
        url = reverse('client-landing')
        return HttpResponseRedirect(url)
