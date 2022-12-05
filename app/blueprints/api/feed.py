import json
import logging

from flask import Blueprint, request, jsonify
from flask_login import current_user

feed = Blueprint('api_feed', __name__, url_prefix='/api/feed')

"""
- People trying to gain unauthorised access to stream (POSSIBLE SOLUTION: require login before accessing stream. Then on server check login details before calling backend api.)
- Registered users trying to exploit the api, e.g. by streaming data to their own sites directly using our api link (POSSIBLE SOLUTION: 
"""


def check_authorisation(campaign):   # TODO This has not been implemented yet. Although this may end up being something that Dave implements on the backend

    """
    Checks if the user is authorised to view the selected client and campaign
    Currently I've set this up assuming that it'd be possible for a user to have access to a client, but not necessarily all of its campaigns and so it checks if they have access to both.
    """

    return True  # temporary until this has been set up on db side

    if ('client' in current_user.clients) and (campaign in current_user.campaigns):
        return True
    else:
        return False


@feed.route('/connect', methods=['POST'])
def connect():

    print('api/getStream called!')

    try:
        request_body = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return 'Failed to get stream.', 404
    else:
        campaign = request_body['campaign']

        if not check_authorisation(campaign):
            return False

        from TLInterface.get_tweet_feed import get_tweet_stream

        tweet_stream = get_tweet_stream(campaign_id=campaign)

        return tweet_stream


@feed.route('/likeTweet', methods=['POST'])
# @login_required
def like_tweet():

    print('api/likeTweet called!')

    try:
        request_body = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return jsonify(False)
    else:
        tweet = request_body['tweet']
        campaign = request_body['campaign']
        like_or_unlike = request_body['like_or_unlike']

    from TLInterface import get_web_connection

    wc = get_web_connection()

    try:
        if like_or_unlike == 'like':
            response = wc.like_tweet(campaign, tweet)
        elif like_or_unlike == 'unlike':
            response = wc.unlike_tweet(campaign, tweet)
        else:
            response = 'Choose either like or unlike tweet.'

        print(response)
        return jsonify(True)
    except Exception as e:
        logging.error(e)
        return jsonify(False)


@feed.route('/saveTweet', methods=['POST'])
def save_tweet():

    print('api/feed/saveTweet called!')

    try:
        request_body = json.loads(request.data)
        tweet_id = request_body['tweetId']
        campaign_id = request_body['campaignId']
    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return jsonify('Failed to get stream.', 404)
    except KeyError as e:
        logging.error(e)
        return jsonify('Failed to get stream.', 404)
    else:
        from TLInterface import get_web_connection
        wc = get_web_connection()
        wc.save_to_locker(
            campaign_id=campaign_id,
            tweet_id=tweet_id
        )
        return jsonify('Success', 200)


@feed.route('/getNewTweets', methods=['POST'])
def get_new_tweets():

    """Api route that fetches the latest tweets and returns them in json format (so the client-side js scripts can understand it)"""

    try:
        request_body = json.loads(request.data)
        next_id = request_body['nextId']
        campaign_id = request_body['campaignId']

        from TLInterface.get_tweet_feed import get_latest_tweets
        response = get_latest_tweets(campaign_id=campaign_id, tweet_id=next_id)

        if response is not False:
            tweets, next_id = response

        return jsonify({
            'status': 200,
            'message': 'Success',
            'data': {
                'tweets': tweets,
                'next_id': next_id
            }
        })

    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return jsonify({
            'status': 400,
            'message': e,
            'data': None
        })

    except Exception as e:
        logging.error(e)
        return jsonify({
            'status': 400,
            'message': e,
            'data': None
        })


@feed.route('/getOldTweets', methods=['POST'])
def get_old_tweets():

    try:

        print('api/feed/getOldTweets called!')

        request_body = json.loads(request.data)

        campaign_id = request_body.get('campaignId')
        page_num = request_body.get('nextPage')
        tweet_cutoff = request_body.get('tweetCutoff')
        num_tweets = request_body.get('numTweets')
        num_pages = request_body.get('numPages')
        ascending = request_body.get('ascending')
        start_score = request_body.get('startScore')
        end_score = request_body.get('endScore')
        start_date = request_body.get('startDate')
        end_date = request_body.get('endDate')
        keywords = request_body.get('keywords')

        from datetime import datetime

        if start_date and end_date:

            # Parsing into datetime format
            start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S%f%z')
            end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S%f%z')

            # Formatting into Dave's format
            start_date = start_date.strftime('%d-%m-%Y')
            end_date = end_date.strftime('%d-%m-%Y')

        print()
        print('Campaign_id:', campaign_id)
        print('Page num:', page_num)
        print('Tweet cutoff:', tweet_cutoff)
        print('Num tweets:', num_tweets)
        print('Num pages:', num_pages)
        print('Ascending:', ascending)
        print('Start score:', start_score)
        print('End score:', end_score)
        print('Start date:', start_date)
        print('End date:', end_date)
        print('Keywords:', keywords)
        print()

        from TLInterface.get_tweet_feed import get_historic_tweets

        response = get_historic_tweets(
            campaign_id=campaign_id,
            ascending=ascending,
            page_num=page_num,
            num_pages=num_pages,
            num_tweets=num_tweets,
            tweet_cutoff=tweet_cutoff,
            start_score=start_score,
            end_score=end_score,
            start_date=start_date,
            end_date=end_date,
            keywords=keywords
        )

        if response:
            tweets, next_page, num_pages, num_tweets = response
            if tweet_cutoff is None and not ascending:
                tweet_cutoff = tweets[0]['id']
            return jsonify({
                'status': 200,
                'message': 'Success',
                'data': {
                    'tweets': tweets,
                    'nextPage': next_page,
                    'numPages': num_pages,
                    'numTweets': num_tweets,
                    'tweetCutoff': tweet_cutoff
                }
            })
        else:
            return jsonify({
                'status': 400,
                'message': 'Failed to get old tweets. Check server logs.',
                'data': None
            })

        # from TLInterface.get_tweet_feed import get_historic_tweets
        # response = get_historic_tweets(campaign_id=campaign_id, next_id=next_id)
        #
        # if response:
        #     tweets, next_id = response

    except json.decoder.JSONDecodeError as e:
        print('FAILED: request_body = json.loads(request.data)')
        print(e)
        return jsonify({
            'status': 400,
            'message': e,
            'data': None
        })

    except Exception as e:
        logging.error(e)
        return jsonify({
            'status': 400,
            'message': e,
            'data': None
        })
