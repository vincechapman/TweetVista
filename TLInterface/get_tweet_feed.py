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

                for tweet in tweets:
                    yield json.dumps(tweet)

                sleep(refresh_rate)  # Could use some maths to adjust the frequency based on the rate of incoming tweets

                # Add function here that checks if the function is live. Would send a get request to an endpoint and set live to False depending on what it returns

        return tweet_generator()

    else:
        return jsonify(False)


if __name__ == '__main__':
    from TLInterface.get_campaigns import get_first_campaign_id

    first_campaign_id = get_first_campaign_id()  # For testing purposes just using the first available campaign id

    tweet_stream = get_tweet_stream(
        campaign_id=first_campaign_id,
        refresh_rate=10
    )

    print(tweet_stream)

    if tweet_stream:
        for tw in tweet_stream:
            print_tweet(tw)
