"""All functions to do with account management can be found in this file."""

from flask import session, has_request_context
from TLInterface import get_web_connection, save_web_connection


def create_account(username: str, firstname: str, lastname: str, email: str, password: str) -> (bool, str):
    """Creates an account in TweetLocator backend."""

    try:
        response = logout_of_account()
        # print(response)
        wc = get_web_connection()
        response = wc.create_client_account(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password)

        if response['status'] == 200:
            save_web_connection(wc)
            return True, response
        else:
            return False, response

    except KeyError:
        return False, 'No response'

    except Exception as e:
        return False, e


def login_to_account(username: str, password: str, wc=None) -> dict:
    """Log in to TweetLocator backend"""

    try:

        if wc is None:
            wc = get_web_connection()

        response = wc.log_user_in(
            username=username,
            password=password)

        if response['status'] == 200:
            wc.userid = username
            wc.password = password
            wc.set_headers()
            save_web_connection(wc)

        return response

    except Exception as e:
        print(e)
        return {}


def logout_of_account():
    """Log out of TweetLocator backend and remove WebConnection object from session"""
    wc = get_web_connection()
    if wc:
        response = wc.logout()
        session.pop('wc')
        session.pop('twitter_handle')
        session.pop('twitter_screen_name')
        session.pop('twitter_profile_image')
        return response
    else:
        print('No WebConnection object found in session.')
        return False


def check_if_logged_in():
    wc = get_web_connection()
    if wc:
        response = wc.is_loggedin()
        return response
    else:
        print('No WebConnection object found in session.')
        return False


if __name__ == '__main__':
    # print(create_account(
    #     username='test5@gmail.com',
    #     firstname='Vince',
    #     lastname='Chapman',
    #     email='test5@gmail.com',
    #     password='changeme'
    # ))

    print(login_to_account(
        username='v.chapman1',
        password='changeme'
    ))

    # print(logout_of_account())

    # print(get_web_connection())
