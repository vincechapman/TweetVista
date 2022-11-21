from TLInterface import get_web_connection

wc = get_web_connection()


def get_saved_tweets(campaign_id):

    response = wc.get_tweet_locker(campaign_id)

    return response


if __name__ == '__main__':

    pass