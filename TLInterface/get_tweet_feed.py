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


def get_historic_tweets(campaign_id: int, next_id: int = 0, page_len: int = 10) -> (dict, int) or False:

    try:
        from TLInterface import get_web_connection
        wc = get_web_connection(username='test10@gmail.com', password='test10')

        response = wc.get_tweets_for_campaign(
            campaign_id=campaign_id,
            page_len=page_len,
            next_id=next_id
        )

        if response['status'] == 200:
            return response['data']['tweets'], response['data']['next_id']
        else:
            print(response['status'])
            return False

    except Exception as e:
        logging.error(e)
        return False


if __name__ == '__main__':

    from pprint import pprint

    pprint(get_historic_tweets(
        campaign_id=47,
        next_id=8752389
    ))
