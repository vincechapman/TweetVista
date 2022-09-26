from flask import Blueprint, render_template, request
from flask_login import login_required

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


class Author(object):

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.username = kwargs['username']
        self.display_name = kwargs['display_name']
        self.profile_image = kwargs['profile_image']

    def __repr__(self):
        return self.id


class Tweet(object):

    def __init__(self, **kwargs):
        from datetime import datetime

        # Tweet ID
        self.id = kwargs['id']

        # Tweet content
        self.text = kwargs['text']

        # Publish time
        self.created_at = datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.000Z')

        # Defining metrics
        self.retweet_count = kwargs['retweet_count']
        self.reply_count = kwargs['reply_count']
        self.like_count = kwargs['like_count']
        self.quote_count = kwargs['quote_count']

        # Media attributes
        self.media = kwargs['media'],

        # Attaching author object
        self.author = Author(
            id=kwargs['author_id'],
            username=kwargs['author_username'],
            display_name=kwargs['author_display_name'],
            profile_image=kwargs['author_profile_image']
        )

    def __repr__(self):
        return self.id


@dashboard.route('/')
def main():

    tweets = None

    if request.method == 'POST':

        search_query = request.form['search-query']

        from twitter_api import collect_tweets, parse_response

        response = collect_tweets(search_query + ' -is:retweet')

        print('RESPONSE:', response)

        if response:
            tweets = parse_response(response)
        else:
            tweets = None

    return render_template('pages/dashboard.html', tweets=tweets)
