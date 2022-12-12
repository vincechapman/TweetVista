import logging
from TLInterface import get_web_connection

wc = get_web_connection(username='test13@gmail.com', password='test13')


def get_saved_tweets(campaign_id) -> list[dict] or False:

    try:

        response = wc.get_tweet_locker(campaign_id)

        if response.get('status') == 200:
            return response.get('data')
        else:
            logging.error(response.get('msg'))
            return False

    except Exception as e:
        logging.error(e)
        return False


if __name__ == '__main__':

    get_saved_tweets(60)
