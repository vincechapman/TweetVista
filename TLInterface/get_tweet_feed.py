import logging


def print_tweet(tweet: dict) -> None:

    from pprint import pprint

    tweet = {
        'id': tweet['id'],
        'twitter_score': tweet['twitter_score'],
        'word_tokens': tweet['word_tokens'],
        'user_handle': tweet['user_handle'],
        'user_id': tweet['user_id'],
        # 'raw': tweet['raw'],
    }

    pprint(tweet, indent=4)


def get_tweet_stream(campaign_id: int, refresh_rate: int = 5):

    """
    Returns a stream that yields fresh tweets periodically

    param:int refresh_rate | Get the latest tweets every x seconds
    """

    import json
    from time import sleep
    from flask import jsonify
    from TLInterface import get_web_connection

    wc = get_web_connection()

    if wc:

        def tweet_generator():
            start_id = 0
            live = True

            while live:
                data = wc.get_page_tweets(campaign_id, tweet_id=start_id, page_len=5)
                tweets = data.get('data', [])

                if tweets:
                    start_id = tweets[0]['id']
                    print(f'NEW TWEETS: {tweets}')
                else:
                    print(f'NO TWEETS CAPTURED.')

                for tweet in tweets:
                    yield json.dumps(tweet)

                sleep(refresh_rate)  # Could use some maths to adjust the frequency based on the rate of incoming tweets

                # Add function here that checks if the function is live. Would send a get request to an endpoint and set live to False depending on what it returns

        return tweet_generator()

    else:
        return jsonify(False)


def get_latest_tweets(campaign_id: int, tweet_id: int = 0) -> (list, int) or False:

    """This function fetches the latest page of tweets since the specified tweet_id. Returns the ID of the last tweet that was captured"""

    try:
        from TLInterface import get_web_connection
        wc = get_web_connection()

        response = wc.get_page_tweets(campaign_id, tweet_id=tweet_id, page_len=100)

        if response.get('status') == 200:

            tweets = response.get('data', [])

            if tweets:
                tweet_id = tweets[0]['id']

            return tweets, tweet_id

        else:
            logging.error(f'Status code: {response.get("status")}\nMessage: {response.get("msg")}')
            return False

    except Exception as e:
        logging.error(e)
        return False


# TODO THIS FUNCTION NEEDS SOME WORK
def get_historic_tweets(campaign_id: int, page_num: int = 1, page_len: int = 100, start_date: str = None, end_date: str = None, keywords: list = [], ascending: bool = True, start_score: int = None, end_score: int = None, tweet_cutoff: int = None, num_pages: int = None, num_tweets: int = None) -> (dict, int) or False:

    try:
        from TLInterface import get_web_connection
        wc = get_web_connection()

        if num_pages is None:

            data = wc.count_campaign_tweets(campaign_id, key_words=keywords, start_date=start_date, end_date=end_date, start_score=start_score, end_score=end_score)

            if data.get('status') != 200:
                print(data.get('status'))
                print(data.get('msg'))
                return False

            num_tweets = data.get('data', 0)
            num_pages = (num_tweets // page_len) + (1 if num_tweets % page_len > 0 else 0)

        tweet_sort = 'asc' if ascending else 'desc'

        response = wc.get_page_of_tweets(
            campaign_id=campaign_id,
            page_no=page_num,
            page_len=page_len,
            start_date=start_date,
            end_date=end_date,
            key_words=keywords,
            tweet_sort=tweet_sort,
            start_score=start_score,  # TODO Test TS start score filter is working
            end_score=end_score,  # TODO Test end score is working + Test with start score
            tweet_cutoff=tweet_cutoff)  # TODO Test this works for latest first mode (which I believe is descending

        if response['status'] == 200:
            if page_num + 1 <= num_pages:
                return response['data']['tweets'], page_num + 1, num_pages, num_tweets
            else:
                logging.info('Got all pages')
                return False
        else:
            print(response['status'])
            print(response['msg'])
            return False

    except Exception as e:
        logging.error(e)
        return False


if __name__ == '__main__':

    campaign_id = 53
    page_num = 1
    looping = True
    tweet_cutoff = None
    num_tweets = None
    num_pages = None
    ascending = True

    while looping:

        print()
        print('Page number:', page_num)
        print('Tweet cutoff:', tweet_cutoff)
        print('Number of tweets:', num_tweets)
        print('Number of pages:', num_pages)

        response = get_historic_tweets(
            campaign_id=campaign_id,
            ascending=ascending,
            page_num=page_num,
            num_pages=num_pages,
            num_tweets=num_tweets,
            tweet_cutoff=tweet_cutoff)

        if response:
            tweets, page_num, num_pages, num_tweets = response
            if tweet_cutoff is None and not ascending:
                tweet_cutoff = tweets[0]['id']
        else:
            looping = False
