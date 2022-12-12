import logging

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required

locker = Blueprint('tweet_locker', __name__, url_prefix='/locker')


@locker.route('/', methods=['GET'])
def main():
    return render_template('pages/tweet_locker/main.html')


@locker.route('/<int:campaign_id>', methods=['GET', 'POST'])
def view_campaign_locker(campaign_id):

    from TLInterface.tweet_locker import get_saved_tweets
    saved_tweets = get_saved_tweets(campaign_id)

    if request.method == 'POST':
        return jsonify(saved_tweets) if saved_tweets else jsonify(False)

    else:
        return render_template('pages/tweet_locker/view_locker.html', saved_tweets=saved_tweets)

