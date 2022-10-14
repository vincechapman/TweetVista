import json
from requests_oauthlib import OAuth1Session
from urllib.parse import quote

import logging
log = logging.getLogger(__name__)

def twitter_get_oauth_request_token(cs,ck,callback):
    consumer_key = ck
    consumer_secret = cs
    request_token = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret,callback_uri=callback)
    url = 'https://api.twitter.com/oauth/request_token'
    data = request_token.get(url)
    if data.status_code != 200:
        log.error('twitter_get_oauth_request_token: status_code: {0} msg: {1}'.format(data.status_code,data.text))
        return [None,None]
#   print(data.text)
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')
    resource_owner_key = ro_key[1]
    resource_owner_secret = ro_secret[1]
    resource = [resource_owner_key, resource_owner_secret]
    return resource


def twitter_get_oauth_token(verifier, twitter_app):
    ro_key = twitter_app['resource_owner_key']
    ro_secret = twitter_app['resource_owner_secret']
    consumer_key = twitter_app['consumer_key']
    consumer_secret = twitter_app['consumer_secret']
    oauth_token = OAuth1Session(client_key=consumer_key,
                                client_secret=consumer_secret,
                                resource_owner_key=ro_key,
                                resource_owner_secret=ro_secret)

    url = 'https://api.twitter.com/oauth/access_token'
    data = {"oauth_token": ro_key,"oauth_verifier": verifier}
    access_token_data = oauth_token.post(url, data=data)

    access_token_list = str.split(access_token_data.text, '&')
    return access_token_list


def twitter_get_access_tokens(access_token_list,twitter_auth_app):
    access_token_key = str.split(access_token_list[0], '=')
    access_token_secret = str.split(access_token_list[1], '=')
    access_token_name = str.split(access_token_list[3], '=')
    access_token_id = str.split(access_token_list[2], '=')
    key = access_token_key[1]
    secret = access_token_secret[1]
    name = access_token_name[1]
    id = access_token_id[1]
    access_tokens = {'id':id,
                     'handle':name,
                     'consumer_key':twitter_auth_app['consumer_key'],
                     'consumer_secret':twitter_auth_app['consumer_secret'],
                     'access_token_key':key,
                     'access_token_secret':secret}
    return access_tokens


def verify_twitter_credentials(access_tokens):
    oauth_user = OAuth1Session(client_key=access_tokens['consumer_key'],
                               client_secret=access_tokens['consumer_secret'],
                               resource_owner_key=access_tokens['access_token_key'],
                               resource_owner_secret=access_tokens['access_token_secret'])
    url_user = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    user_data = oauth_user.get(url_user)
    user_data = user_data.json()
    return user_data


def construct_twitter_callback(request):
    headers=request.META
    #log.info('Request Headers {0}'.format(headers))
    scheme = headers.setdefault('HTTP_X_FORWARDED_PROTOCOL','http')
    scheme=scheme.lower()
    #callback = '{0}://{1}{2}'.format(scheme,request.headers.get('host',''),'/twitter/login/callback/')
    callback = f'{scheme}://{request.headers.get("host","")}{"/twitter/login/callback/"}'
    log.info('Callback: {0}'.format(callback))
    return callback


def get_twitter_account_details(handle):
    pass


if __name__=='__main__':
    res=twitter_get_oauth_request_token()
    with open('request_token.json','w') as fl:
        json.dump(res,fl)
