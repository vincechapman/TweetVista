import json
import logging

from flask import Blueprint, render_template, request, jsonify, current_app, Response
from flask_login import login_required, current_user

feed = Blueprint('api_feed', __name__, url_prefix='/api/feed')

"""
- People trying to gain unauthorised access to stream (POSSIBLE SOLUTION: require login before accessing stream. Then on server check login details before calling backend api.)
- Registered users trying to exploit the api, e.g. by streaming data to their own sites directly using our api link (POSSIBLE SOLUTION: 
"""


def check_authorisation(client, campaign):

    """
    Checks if the user is authorised to view the selected client and campaign
    Currently I've set this up assuming that it'd be possible for a user to have access to a client, but not necessarily all of its campaigns and so it checks if they have access to both.
    """

    return True  # temporary until this has been set up on db side

    if (client in current_user.clients) and (campaign in current_user.campaigns):
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
        client = request_body['client']
        campaign = request_body['campaign']

        if not check_authorisation(client, campaign):
            return False

        from TLInterface.get_tweet_feed import get_tweet_stream

        tweet_stream = get_tweet_stream(campaign_id=campaign)

        # # Note that the front end stream won't run it this for loop is uncommented
        # if tweet_stream:
        #     for t in tweet_stream:
        #         print(t)

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
        return 'Failed to get stream.', 404
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
