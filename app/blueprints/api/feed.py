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
        request_body = json.loads(request.data)
        next_id = request_body['nextId']
        campaign_id = request_body['campaignId']

        from TLInterface.get_tweet_feed import get_historic_tweets
        response = get_historic_tweets(campaign_id=campaign_id, next_id=next_id)

        if response:
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
