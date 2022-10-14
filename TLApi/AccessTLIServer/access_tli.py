import json
import logging
import pprint
import time
import os
from dotenv import load_dotenv
load_dotenv()

from TLApi.HTTPAccess.webconn_singleton import WebConnection

__author__ = 'dhagan'
log = logging.getLogger('access_tli')
log.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)


def test_login_conn():
    wc = web_conn()
    ret_dict = wc.get_client_campaigns()
    data = ret_dict.get('data',[])
    if len(data) > 0:
        for dt in data:
            pprint.pprint(dt, indent=4)
        campaign = data[0]
        pprint.pprint(campaign, indent=4)
        campaign_id = campaign.get('id', '0')
        ret_dict = wc.get_client_campaign_by_id(campaign_id)
        data = ret_dict.get('data', {})
        pprint.pprint(data, indent=4)

        # get tweets
        id = 0
        for cnt in range(10):
            data = wc.get_page_tweets(campaign_id,tweet_id=id,page_len=5)
            tweets = data.get('data',[])
            if len(tweets) > 0:
                id = tweets[0]['id']
            for tweet in tweets:
                print_basic(tweet)
            time.sleep(5)


def print_basic(tweet):
    tw={'id':tweet['id'],
        'twitter_score':tweet['twitter_score'],
        'word_tokens':tweet['word_tokens'],
        'user_handle':tweet['user_handle'],
        'user_id':tweet['user_id']}
    pprint.pprint(tw, indent=4)


def get_key_lits():
    wc = web_conn()
    data = wc.get_keyword_literals()
    pass


def create_campaign(campaign):
    wc = web_conn()
    ret = wc.create_campaign_from_json(campaign)


def get_campaign(campaign_id):
    wc = web_conn()
    ret_dict = wc.get_client_campaign_by_id(campaign_id)
    if ret_dict.get('status', 404) == 200:
        return ret_dict.get('data', {})
    else:
        return {}


def authenticate_user():

    wc = web_conn(url='https://tlapi.ictbenchmark.org/', usr=os.environ['WEB_CONN_USER'], pwd=os.environ['WEB_CONN_PASSWORD'])
    ret_dict = wc.authenticate_user()
    sessionid = wc.get_sessionid()
    if sessionid is not None:
        log.info(f'sessionid={sessionid}')
    log.info(f'{ret_dict}')
    wc = web_conn(sessionid=sessionid)
    ret_dict = wc.is_authenticated()
    log.info(f'{ret_dict}')
    pass


def web_conn(usr=None, pwd=None, url=None, sessionid=None):
    wc = WebConnection(
        userid=usr,
        password=pwd,
        url=url,
        sessionid=sessionid
    )
    return wc


if __name__ == '__main__':

    authenticate_user()
    test_login_conn()
