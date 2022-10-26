from django import forms
from django.conf import settings
from TLAPIWebTest.data.utils.messaging import MessageMixin
from TLAPIWebTest.tlapi.web.webconn_singleton import WebConnection


class LoginForm(MessageMixin,forms.Form):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput)
    password = forms.CharField(max_length=100,required=True,widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('username')
        pwd = cleaned_data.get('password')
        wc = WebConnection(url=settings.TLAPI_URL,userid=user,password=pwd)
        wc.set_headers()
        ret_dict = wc.log_user_in()
        if ret_dict.get('status',404) == 200:
            tlapi_session_id = wc.get_sessionid()
            self.request.session['tlapi_session_id']=tlapi_session_id
        else:
            self.error(ret_dict.get('msg','Not Authenticated'), request=self.request)
            raise forms.ValidationError(
                ret_dict.get('msg','Not Authenticated')
            )


