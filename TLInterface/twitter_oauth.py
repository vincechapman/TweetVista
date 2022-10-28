import logging
from pprint import pprint

import requests
from requests_oauthlib import OAuth1Session
from flask import request, Flask, redirect, url_for, session, Response, jsonify
from flask_login import current_user
import models


def get_app_credentials() -> dict or {}:
    """
    This function returns the name of the app as well as its consumer key, consumer secret and callback route.
    It is called when the app it initialised in order to create the twitter callback route.
    As well as returning the app details, it also saves them to Flask's session object, so we can access them later on
    without having to call this function again.
    """

    from TLInterface import get_web_connection
    wc = get_web_connection()
    try:
        response = wc.get_twitter_app()
        status = response.get('status', 404)
        if status == 200:
            data = response.get('data', {})
            return data
        else:
            logging.error(f'Status code: {status}')
            return {}
    except Exception as e:
        logging.error(e)
        return {}


def get_resource_owner_credentials(consumer_key, consumer_secret, callback) -> tuple[str, str]:
    """This function returns resource owner key and secret"""

    oauth_request = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret, callback_uri=callback)
    request_token = oauth_request.get('https://api.twitter.com/oauth/request_token')

    if request_token.status_code != 200:
        # "Any value other than 200 indicates a failure."
        return '', ''

    request_token = str.split(request_token.text, '&')

    oauth_token = str.split(request_token[0], '=')[1]
    oauth_token_secret = str.split(request_token[1], '=')[1]
    oauth_callback_confirmed = str.split(request_token[2], '=')[1]

    if oauth_callback_confirmed != 'true':
        return '', ''

    return oauth_token, oauth_token_secret


def get_access_tokens(oauth_token, oauth_verifier, twitter_app):
    """Uses oauth_token and oauth_verifier to obtain usable access tokens that will be used for future requests to the Twitter api."""

    ro_key = twitter_app['resource_owner_key']
    # ro_secret = twitter_app['resource_owner_secret']

    consumer_key = twitter_app['consumer_key']
    consumer_secret = twitter_app['consumer_secret']

    # oauth_token = OAuth1Session(
    #     client_key=consumer_key,
    #     client_secret=consumer_secret,
    #     resource_owner_key=ro_key,
    #     resource_owner_secret=ro_secret)

    # Sending request to POST oauth/access_token
    s = requests.Session()
    url = 'https://api.twitter.com/oauth/access_token'
    data = {"oauth_consumer_key": consumer_key, "oauth_token": oauth_token, "oauth_verifier": oauth_verifier}
    response = s.post(url, data=data)

    # Parsing response
    access_token_list = str.split(response.text, '&')
    access_token_key = str.split(access_token_list[0], '=')[1]
    access_token_secret = str.split(access_token_list[1], '=')[1]
    twitter_handle = str.split(access_token_list[3], '=')[1]
    access_token_id = str.split(access_token_list[2], '=')[1]

    access_tokens = {
        'id': access_token_id,
        'handle': twitter_handle,
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'access_token_key': access_token_key,
        'access_token_secret': access_token_secret}

    return access_tokens


def verify_twitter_credentials(access_tokens):

    """
    This function verifies that the twitter credentials we have are valid.
    More info on this here: https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/manage-account-settings/api-reference/get-account-verify_credentials
    """

    s = OAuth1Session(
        client_key=access_tokens['consumer_key'],
        client_secret=access_tokens['consumer_secret'],
        resource_owner_key=access_tokens['access_token_key'],
        resource_owner_secret=access_tokens['access_token_secret'])

    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'

    response = s.get(url)
    return response.json()


def build_routes(app: Flask) -> None:

    """Builds Flask callback route using route provided by get_app_credentials()"""

    # Callback Route

    app_data = get_app_credentials()

    if app_data:
        callback_route = app_data['callback']

        @app.route(callback_route, methods=['GET', 'POST'])  # TODO is the callback request POST or GET, for now allow both.
        def twitter_oauth_callback():
            query_params = request.args
            oauth_token = query_params['oauth_token']
            oauth_verifier = query_params['oauth_verifier']

            twitter_app = session.pop('twitter_app', default=None)
            if twitter_app is None:
                logging.error('Cannot get twitter app data from session')
                return redirect(url_for('index'))

            access_tokens = get_access_tokens(oauth_token, oauth_verifier, twitter_app)

            only_tokens = {i: access_tokens[i] for i in access_tokens}
            only_tokens['user_data'] = verify_twitter_credentials(access_tokens)
            only_tokens['app_name'] = twitter_app.get('app_name', None)
            only_tokens['target_id'] = None

            from TLInterface import get_web_connection
            wc = get_web_connection()
            data = wc.store_user_twitter_account(only_tokens)
            logging.info(f"{only_tokens['app_name']} authorised {only_tokens['handle']}")

            print(only_tokens)

            current_user.twitter_handle = only_tokens.get('handle')
            current_user.twitter_screen_name = only_tokens.get('user_data').get('screen_name')
            current_user.twitter_profile_image = only_tokens.get('user_data').get('profile_image_url')
            models.db.session.commit()

            session['twitter_connected'] = only_tokens['handle']

            return """
                This popup should close itself
            """

        logging.info('Successfully created twitter callback route.')

    else:
        logging.error('Failed to create twitter callback route.')

    # User authorisation route

    @app.route('/twitter/auth')
    def authorise_account() -> Response or bool:

        logging.info('Started twitter oauth process.')

        try:
            twitter_app = get_app_credentials()

            if twitter_app:
                name = twitter_app['name']
                consumer_key = twitter_app['consumer_key']
                consumer_secret = twitter_app['consumer_secret']
                callback = request.host_url[:-1] + twitter_app['callback']

                oauth_token, oauth_token_secret = get_resource_owner_credentials(
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    callback=callback)

                if '' in [oauth_token, oauth_token_secret]:
                    logging.error('Failed to get resource owner credentials.')
                    return jsonify(False)

                twitter_app = {
                    'app_name': name,
                    'consumer_key': consumer_key,
                    'consumer_secret': consumer_secret,
                    'resource_owner_key': oauth_token,
                    'resource_owner_secret': oauth_token_secret}

                session['twitter_app'] = twitter_app

                url = 'https://api.twitter.com/oauth/authorize?oauth_token=' + oauth_token + '&force_login=true'
                return jsonify(url)

            else:
                raise Exception('get_app_credentials returned empty dictionary.')

        except Exception as e:
            print(e)

        return jsonify(False)

    @app.route('/twitter/auth/check')
    def check_if_twitter_authorised():

        twitter_connected = session.get('twitter_connected')
        if twitter_connected and twitter_connected == current_user.twitter_handle:  # TODO need to check the twitter in session matches the account logging in
            twitter_user = {
                'handle': current_user.twitter_handle,
                'screenName': current_user.twitter_screen_name,
                'profileImage': current_user.twitter_profile_image}
            logging.info('Twitter account is already authorised.')
            return jsonify(twitter_user)
        else:
            logging.warning('Twitter account not currently authorised. Authorise via Twitter Oauth.')
            return jsonify(False)
