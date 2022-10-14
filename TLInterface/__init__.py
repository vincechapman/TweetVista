"""
This module serves as an intermediary between my frontend application and Dave's API.
"""

import logging
from TLApi.AccessTLIServer.access_tli import WebConnection, web_conn, authenticate_user


def get_web_connection() -> WebConnection or bool:

    # Line here that checks if there is already a wc saved in session object, if so return that. Otherewise return below code.

    try:
        authenticate_user()
    except Exception as e:
        logging.error(f'Failed to authenticate user, due to following error:\n\n{e}')
        return False

    try:
        wc = web_conn()
    except Exception as e:
        logging.error(f'Failed to create web connection, due to following error:\n\n{e}')
        return False
    else:
        # Add an option here for saving wc to a session object if doesn't already exist
        return wc
