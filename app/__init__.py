import logging
import os
from dotenv import load_dotenv
from flask import Flask, session, redirect, url_for
from flask_login import LoginManager


# Making environment variables accessible in this script
load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ['FLASK_SECRET'],
        SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DATABASE_URI'],
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    from models import db, User
    db.init_app(app)

    @app.route('/hello')
    def hello_world():  # put application's code here
        return 'Hello World!'

    # Setting up login_manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Setting up homepage
    homepage = 'campaigns.main'

    # app.add_url_rule('/', endpoint=homepage, methods=['GET', 'POST'])

    @app.route('/index', methods=['GET', 'POST'])
    def index():
        return redirect(url_for(homepage))

    @app.route('/', methods=['GET', 'POST'])
    def homepage_redirect():
        return redirect(url_for(homepage))


    # Registering blueprints
    from . blueprints.dashboard import dashboard as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from . blueprints.campaigns import campaigns as campaigns_bp
    app.register_blueprint(campaigns_bp)

    from . blueprints.api.feed import feed as api_feed_bp
    app.register_blueprint(api_feed_bp)

    from . blueprints.api.campaigns import api_campaigns as api_campaign_bp
    app.register_blueprint(api_campaign_bp)

    from . blueprints.api.auth import auth as api_auth_bp
    app.register_blueprint(api_auth_bp)

    from . blueprints.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from . blueprints.tweet_locker import locker as locker_bp
    app.register_blueprint(locker_bp)

    # Add twitter authorisation routes
    from TLInterface.twitter_oauth import build_routes
    build_routes(app)

    return app
