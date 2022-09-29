import json

from flask import Blueprint, render_template, request, jsonify, current_app, Response
from flask_login import login_required, current_user

api = Blueprint('api', __name__, url_prefix='/api')

"""
- People trying to gain unauthorised access to stream (POSSIBLE SOLUTION: require login before accessing stream. Then on server check login details before calling backend api.)
- Registered users trying to exploit the api, e.g. by streaming data to their own sites directly using our api link (POSSIBLE SOLUTION: 
"""


def check_authorisation(client, campaign):

    """
    Checks if the user is authorised to view the selected client and campaign
    Currently I've set this up assuming that it'd be possible for a user to have access to a client, but not necessarily all of its campaigns and so it checks if they have access to both.
    """

    if (client in current_user.clients) and (campaign in current_user.campaigns):
        return True
    else:
        return False


@api.route('/getStream', methods=['GET', 'POST'])
def get_stream():

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

        # if not check_authorisation(client, campaign):
        #     return False

        from TLApi.AccessTLIServer.access_tli import authenticate_user, run_stream

        authenticate_user()

        return run_stream(campaign)
