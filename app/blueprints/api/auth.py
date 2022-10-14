import json
import models

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('api_auth', __name__, url_prefix='/api/auth')


@auth.route('/signup', methods=['POST'])
def signup():

    """The client sends signup details to this route and this function creates an account for them."""

    request_body = json.loads(request.data)

    new_user_obj = models.User(
        first_name=request_body['first_name'],
        last_name=request_body['last_name'],
        company_name=request_body['company_name'],
        email_address=request_body['email_address'],
        password=generate_password_hash(request_body['password'])
    )

    try:
        models.db.session.add(new_user_obj)
        models.db.session.commit()
        login_user(new_user_obj, remember=True)

    except Exception as e:
        print(e)
        if 'UNIQUE constraint failed: user.email_address' in str(e):
            return jsonify({
                'success': False,
                'message': "An account is already registered with this email address. Would you like to login instead?"})
        elif 'NOT NULL constraint failed' in str(e):
            return jsonify({
                'success': False,
                'message': "Please check you have provided all required details."})
        else:
            return jsonify({
                'success': False,
                'message': "Account not created. Server side error."})

    else:
        return jsonify({
            'success': True,
            'message': "Account created"})


@auth.route('/login', methods=['POST'])
def login():

    """The client sends login details to this route and this function signs them in"""

    request_body = json.loads(request.data)

    user_obj = models.User.query.filter_by(email_address=request_body['email_address']).first()

    if not user_obj:
        return jsonify({
            'success': False,
            'message': "No account registered with this email address."})
    elif not check_password_hash(user_obj.password, request_body['password']):
        return jsonify({
            'success': False,
            'message': "Password incorrect."})

    try:
        login_user(user_obj, remember=True)

    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': "Account not logged in. Server side error."})

    else:
        return jsonify({
            'success': True,
            'message': "Account logged in."})
