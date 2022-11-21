import json
import models
import logging

from flask import Blueprint, request, jsonify, has_request_context, session
from flask_login import login_user, login_required, current_user

auth = Blueprint('api_auth', __name__, url_prefix='/api/auth')


@auth.route('/signup', methods=['POST'])
def signup():

    """The client sends signup details to this route and this function creates an account for them."""

    request_body = json.loads(request.data)
    email_address = request_body['email_address']
    first_name = request_body['first_name']
    last_name = request_body['last_name']
    password = request_body['password']

    try:
        from TLInterface import get_web_connection
        wc = get_web_connection()
        data = wc.create_client_account(
            username=email_address,
            firstname=first_name,
            lastname=last_name,
            email=email_address,
            password=password)

        status = data.get('status', 404)

        print(data)

        if status == 200:
            from TLInterface.auth import login_to_account
            response = login_to_account(email_address, password)
            if response.get('status') == 200:
                if has_request_context():
                    session['logged_in'] = True
                return jsonify({
                    'success': True,
                    'message': "Account created and logged in."})
            else:
                return jsonify({
                    'success': False,
                    'message': "Account created but not logged in."})
        elif status == 404 and 'Exists' in data.get('msg'):
            return jsonify({
                'success': False,
                'message': "Account already exists. Please log in instead."})
        else:
            print(data)
            return jsonify({
                'success': False,
                'message': "Unknown error."
            })

    except Exception as e:

        if 'unique' in str(e) and 'user_email_address_key' in str(e):
            return jsonify({
                'success': False,
                'message': "An account is already registered with this email address. Would you like to login instead?"})

        elif 'NOT NULL constraint failed' in str(e):
            return jsonify({
                'success': False,
                'message': "Please check you have provided all required details."})

        else:
            print(e)
            return jsonify({
                'success': False,
                'message': "Account not created. Server side error."})

    else:
        return jsonify({
            'success': False,
            'message': "Account not created. Unknown error."})


@auth.route('/login', methods=['POST'])
def login():

    """The client sends login details to this route and this function signs them in"""

    request_body = json.loads(request.data)
    email_address = request_body['email_address']
    password = request_body['password']

    try:
        from TLInterface.auth import login_to_account
        response = login_to_account(
            username=email_address,
            password=password)  # TODO: Eventually implement password hashing/encryption
        print(response)

        if response['status'] == 200:
            print('Success!')

            if has_request_context():
                session['logged_in'] = True

            from TLInterface import get_web_connection
            wc = get_web_connection()

            print('\nChecking if twitter account set:')
            response = wc.is_twitter_account_set()

            # TODO Get Dave to return the twitter details in this response and then save them to the session object below

            if response.get('status') == 200:
                return jsonify({
                    'success': True,
                    'message': "Successfully logged in to account and valid twitter credentials found.",
                    'twitterCredentialsFound': True
                })
            else:
                print(response)
                return jsonify({
                    'success': True,
                    'message': "Successfully logged in to account but valid twitter credentials not found.",
                    'twitterCredentialsFound': False
                })

        else:
            return jsonify({
                'success': False,
                'message': "Account details not recognised."})

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': "Account not logged in. Server side error."})


@auth.route('/businessDetails', methods=['POST'])
def store_business_details():

    try:
        request_body = json.loads(request.data)

        if request_body['company_name']:
            current_user.company_name = request_body['company_name']

        if request_body['company_size']:
            current_user.company_size = request_body['company_size']

        if request_body['role_in_company']:
            current_user.role_in_company = request_body['role_in_company']

        current_user.business_information_provided = True
        current_user.onboarded = True
        models.db.session.commit()

    except Exception as e:
        logging.error(e)
        models.db.session.rollback()
        return jsonify({
            'success': False,
            'message': "Failed to save business details to database."})

    else:
        return jsonify({
            'success': True,
            'message': "Saved business details for current user."})


@auth.route('/getSessionLogin', methods=['POST'])
def check_if_logged_in():
    try:
        from TLInterface import get_web_connection
        wc = get_web_connection()
        if wc.userid and wc.password:
            print(f'Username: {wc.userid}\nPassword: {wc.password}')
            return jsonify({
                'status': 200,
                'message': 'Login credentials retrieved from session',
                'data': wc.userid
            })
        else:
            message = 'No login credentials found in session'
            print(message)
            return jsonify({
                'status': 404,
                'message': message,
                'data': None
            })
    except Exception as e:
        logging.error(e)
        return jsonify({
            'status': 404,
            'message': 'Check error logs',
            'data': None
        })
