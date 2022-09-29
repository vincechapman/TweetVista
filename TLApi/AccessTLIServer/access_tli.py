import json
import logging
import pprint

if __name__ == '__main__':
    from TLApi.HTTPAccess.webconn_singleton import WebConnection
else:
    from .. HTTPAccess.webconn_singleton import WebConnection

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
        campaign_id = campaign.get('id','0')
        ret_dict = wc.get_client_campaign_by_id(campaign_id)
        data = ret_dict.get('data', {})
        pprint.pprint(data, indent=4)
        data = wc.get_page_tweets( campaign_id, 10)
        tweets = data.get('data',[])
        for tweet in tweets:
            pprint.pprint(tweet, indent=4)
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
    if ret_dict.get('status',404) == 200:
        return ret_dict.get('data',{})
    else:
        return {}


def run_stream(campaign_id):

    import json

    wc = web_conn()

    for tweet in wc.get_twitter_stream(campaign_id):

        tweet_json = json.loads(tweet)
        tweet_json_string = json.dumps(tweet_json)
        yield tweet_json_string


def authenticate_user():

    wc = web_conn(url='https://tlapi.ictbenchmark.org/', usr='d.hagan', pwd='changeme')
    ret_dict = wc.authenticate_user()
    sessionid = wc.get_sessionid()
    if sessionid is not None:
        log.info(f'sessionid={sessionid}')
    log.info(f'{ret_dict}')
    wc = web_conn(sessionid=sessionid)
    ret_dict = wc.is_authenticated()
    log.info(f'{ret_dict}')

    return wc


def web_conn(usr=None, pwd=None, url=None, sessionid=None):
    wc = WebConnection(
        userid=usr,
        password=pwd,
        url=url,
        sessionid=sessionid
    )
    return wc


def main():

    authenticate_user()
    run_stream()

    for count, i in enumerate(run_stream(), start=1):
        print(count, i)


if __name__ == '__main__':

    main()




