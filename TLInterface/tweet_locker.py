from TLInterface import get_web_connection

wc = get_web_connection(username='test10@gmail.com', password='test10')


def get_saved_tweets(campaign_id):

    response = wc.get_tweet_locker(campaign_id)

    return response


if __name__ == '__main__':

    pass