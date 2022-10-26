from django.conf import settings
from django.http import HttpResponseRedirect

from TLAPIWebTest.tlapi.web.webconn_singleton import WebConnection


class LoginMixin:
    def dispatch(self, request, *args, **kwargs):
        sessionid = request.session.get('tlapi_session_id',None)
        if sessionid is not None:
            wc = WebConnection(url=settings.TLAPI_URL,sessionid=sessionid)
            ret_dict = wc.is_authenticated()
            if ret_dict.get('status',404) == 200:
                return super().dispatch(request, *args, **kwargs)

        path_info = request.META.get('PATH_INFO')
        return HttpResponseRedirect(f'/auth/login/?next={path_info}')

