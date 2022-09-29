from flask import Blueprint, render_template, request, g
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

    """This is a basic stream that uses yield to stream the tweets directly into a plain html file."""

    from TLApi.AccessTLIServer.access_tli import authenticate_user, test_login_conn, run_stream

    # This only creates a new web connection if one does not already exist globally
    if 'wc' not in g:
        g.wc = authenticate_user()

    try:
        data = g.wc.get_client_campaigns()
    except Exception as e:
        print(e)
        campaigns = None
    else:
        campaigns = data.get('data', [])

    return render_template('pages/dashboard.html', campaigns=campaigns)
