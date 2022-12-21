"""
This module serves as an intermediary between my frontend application and Dave's API.
"""

import logging
from TLApiWeb.connect import WebConnection
from flask import session, has_request_context
import pickle


def authenticate_user(user: str, password: str) -> WebConnection:
    wc = WebConnection()
    if wc.url is None:
        wc.url = 'https://tlapi.ictbenchmark.org/'
    wc.userid = user
    wc.password = password
    wc.set_headers()
    ret_dict = wc.authenticate_user()
    logging.info(f'{ret_dict}')
    ret_dict = wc.is_authenticated()
    return wc


def web_conn(usr=None, pwd=None, url=None, sessionid=None):
    wc = WebConnection(
        userid=usr,
        password=pwd,
        url=url,
        sessionid=sessionid
    )
    return wc


# TODO: Change this function so it doesn't use dave's tweet locator login details. This will require me to first add the create client account function that dave added.
def get_web_connection(username: str = None, password: str = None) -> WebConnection or False:

    """This function creates a new WebConnection object, or fetches it from session object if it already exists."""

    try:
        url = 'https://tlapi.ictbenchmark.org/'
        wc = session.get('wc') if has_request_context() else None

        if wc:
            wc = pickle.loads(wc)
            print('Returning WebConnection saved in session.: ', wc.__dict__)

            if wc.userid and wc.password:
                response = wc.authenticate_user()
                logging.info(f'{response}')

        else:
            wc = WebConnection(userid=None, password=None, url=None, sessionid=None)
            wc.userid = username
            wc.password = password
            wc.set_headers()
            print('Created new WebConnection: ', wc.__dict__)
        if wc.url is None:
            wc.url = url
        save_web_connection(wc)
        return wc
    except Exception as e:
        print(f'Failed to create web connection, due to following error:\n\n{e}')
        return False


def save_web_connection(wc):
    try:
        if has_request_context():
            session['wc'] = pickle.dumps(wc)
            print('Saved WebConnection to session.')
    except Exception as e:
        print(e)
        return False
    else:
        return True
