import json
import logging
import pprint

__author__ = 'dhagan'
log = logging.getLogger('TLApi_Singleton')
log.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
import requests

class InvalidHttpResponse(Exception):
    status_code = -1
    value = ''

    def __init__(self, value, status_code):
        self.status_code = status_code
        super().__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)

    def get_status(self):
        return self.status_code


class InvalidLogin(Exception):
    def __init__(self, value):
        super(InvalidLogin, self).__init__(value)
        self.value = value

    def __str__(self):
        return repr(self.value)


class NotLoggedIn(Exception):
    def __init__(self, value, status_code):
        super(NotLoggedIn, self).__init__(value)
        self.value = value
        self.status_code = status_code

    def __str__(self):
        return repr(self.value)

    def get_status(self):
        return self.status_code


def display_dict(dict_data):
    pprint.pprint(dict_data, indent=4)


class WebConnection:
    __logged_in = False
    streams = {}
    instance = None
    _userid = None
    _password = None
    _url = None
    _sessionid = None
    _session = None

    def __new__(cls, **kwargs):
        if cls.instance is None:
            log.info(f'Starting WebConnection Singleton')
            cls.instance = super().__new__(cls)

        if cls.instance._userid is None:
            cls.instance._userid = kwargs.get('userid', None)

        if cls.instance._password is None:
            cls.instance._password = kwargs.get('password', None)

        if cls.instance._url is None:
            cls.instance._url = kwargs.get('url', None)

        if cls.instance._sessionid is None:
            cls.instance._sessionid = kwargs.get('sessionid', None)
        if cls.instance._session is None:
            cls.instance._session = requests.session()
        return cls.instance

    @property
    def userid(self):
        return self._userid

    @userid.setter
    def userid(self, value):
        self._userid = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def sessionid(self):
        return self._sessionid

    @sessionid.setter
    def sessionid(self, value):
        self._sessionid = value

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    def set_headers(self):
        self._session.headers.update({'TLApi-Auth': 'True'})
        self._session.headers.update({'TLApi-User': self._userid})
        self._session.headers.update({'TLApi-Pass': self._password})

    def authenticate_user(self):
        ret_val = False
        sessionid = self.get_sessionid()
        if sessionid is not None:
            requests.utils.add_dict_to_cookiejar(self._session.cookies,{'sessionid':sessionid})
        else:
            self.set_headers()
        r = self._session.post(self.url + 'common/auth_user/')
        ret_val = json.loads(r.text)
        return ret_val

    def is_authenticated(self):
        ret_val = False
        sessionid = self.get_sessionid()
        if sessionid is not None:
            requests.utils.add_dict_to_cookiejar(self._session.cookies,{'sessionid':sessionid})
        else:
            self.set_headers()
        r = self._session.post(self.url + 'common/is_auth_user/')
        ret_val = json.loads(r.text)
        return ret_val

    def logout(self):
        r = self._session.post(self.url + 'common/user_logout/')
        status = r.status_code
        try:
            data = json.loads(r.text)
        except Exception as msg:
            data = {"success": False, "error": f'{msg}'}

        return data

    def log_user_in(self):
        r = self._session.post(self.url + 'common/user_login/')
        try:
            data = json.loads(r.text)
        except Exception as msg:
            data = {"success": False, "error": f'{msg}'}
        return data

    def is_loggedin(self):
        ret_val = False
        r = self._session.post(self.url + 'common/is_user_loggedin/')
        if r.status_code == 200:
            self.__logged_in = True
            ret_val = True
        else:
            self.__logged_in = False
        return ret_val

    def get_client_campaigns(self):
        r = self._session.post(self.url + 'client/get_campaigns/')
        data = json.loads(r.text)
        ret_val = data
        return ret_val

    def get_client_campaign_by_id(self, campaign_id):
        values = {'campaign_id': campaign_id}
        r = self._session.post(self.url + 'client/get_campaign/', values)
        data = json.loads(r.text)
        ret_val = data
        return ret_val

    def create_campaign_from_json(self,campaign):
        campaign_json = json.dumps(campaign)
        values = {'campaign_json': campaign_json}
        r = self._session.post(self.url + 'client/create_json_campaign/', values)
        data = json.loads(r.text)
        pass

    def get_twitter_stream(self, campaign_id):
        self.streams[campaign_id] = False
        values = {'campaign_id': campaign_id}
        with self._session.post(self.url + 'client/tweet_stream/', values, headers=None, stream=True) as resp:
            for line in resp.iter_lines(chunk_size=250, decode_unicode=True):
                close_stream = self.streams.get(campaign_id, True)
                if close_stream:
                    resp.close()
                    break
                if line:
                    yield line

    def get_page_tweets(self, campaign_id, page_len=10,tweet_id=None):
        values = {'campaign_id': campaign_id, 'page_len': page_len,'tweet_id':tweet_id}
        r = self._session.post(self.url + 'client/latest_tweets/', values)
        dta = json.loads(r.text)
        if isinstance(dta, dict):
            dta['status'] = r.status_code
        return dta

    def get_keyword_literals(self):
        r = self._session.post(self.url + 'common/keyword_lits/')
        dta = json.loads(r.text)
        data = dta['data']
        status = r.status_code
        if status != 200:
            data = {}
        return data

    def close_stream(self, campaign_id):
        self.streams[campaign_id] = True

    def get_sessionid(self):
        sessionid = None
        if self._sessionid is None:
            s_cookie_jar = self.get_session_cookie()
            if s_cookie_jar is not None:
                self._sessionid = s_cookie_jar.get('sessionid',None)

        return self._sessionid

    def get_session_cookie(self):
        if self._session is not None:
            return self._session.cookies
        return None
