import os
from dotenv import load_dotenv
from flask import Flask

# Making environment variables accessible in this script
load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ['FLASK_SECRET'],
        SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DATABASE_URI'],
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    from .models import db
    db.init_app(app)

    @app.route('/hello')
    def hello_world():  # put application's code here
        return 'Hello World!'

    # Setting up homepage
    homepage = 'dashboard.main'

    app.add_url_rule('/', endpoint=homepage, methods=['GET', 'POST'])

    @app.route('/index', methods=['GET', 'POST'])
    def index():
        from flask import redirect, url_for
        return redirect(url_for(homepage))

    # Registering blueprints
    from . blueprints.dashboard import dashboard as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from . blueprints.api import api as api_bp
    app.register_blueprint(api_bp)

    from . blueprints.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    return app
