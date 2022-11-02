"""
This module serves as an intermediary between my frontend application and Dave's API.
"""

import logging
# from TLApi.AccessTLIServer.access_tli import WebConnection, web_conn, authenticate_user
from TLApiWeb.connect import WebConnection


def authenticate_user(user, password):
    wc = WebConnection()
    if wc.url is None:
        wc.url = 'https://tlapi.ictbenchmark.org/'
    wc.userid = user
    wc.password = password
    wc.set_headers()
    ret_dict = wc.authenticate_user()
    logging.info(f'{ret_dict}')
    ret_dict = wc.is_authenticated()


def web_conn(usr=None, pwd=None, url=None, sessionid=None):
    wc = WebConnection(
        userid=usr,
        password=pwd,
        url=url,
        sessionid=sessionid
    )
    return wc


def get_web_connection(user: str = 'd.hagan', password: str = 'changeme') -> WebConnection or bool:

    try:
        authenticate_user(user, password)
    except Exception as e:
        logging.error(f'Failed to authenticate user, due to following error:\n\n{e}')
        return False

    try:
        wc = web_conn()
    except Exception as e:
        logging.error(f'Failed to create web connection, due to following error:\n\n{e}')
        return False

    return wc
