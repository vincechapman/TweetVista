import logging

log = logging.getLogger(__name__)
class MessageMixin:
    ERROR='error'
    INFO='info'
    WARN='warn'
    DEBUG='debug'

    def __msg(self,level,msg,request=None):
        if request is None:
            return
        error_lst = request.session.get('messages',[])
        error_lst.append({'msg':msg,'msg_level':level})
        request.session['messages']=error_lst
        return

    def error(self,msg,request=None):
        if request is None:
            if self.request is None:
                return
            request=self.request
        self.__msg(MessageMixin.ERROR,msg,request)

    def info(self,msg,request=None):
        if request is None:
            if self.request is None:
                return
            request=self.request
        self.__msg(MessageMixin.INFO,msg,request)

    def warn(self,msg,request=None):
        if request is None:
            if self.request is None:
                return
            request=self.request
        self.__msg(MessageMixin.WARN,msg,request)

    def debug(self,msg,request=None):
        if request is None:
            if self.request is None:
                return
            request=self.request
        self.__msg(MessageMixin.DEBUG,msg,request)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        messages=self.request.session.pop('messages',[])
        log.info('Message:{0}'.format(messages))
        context['messages']=messages
        return context
