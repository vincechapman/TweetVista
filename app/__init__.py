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

    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'

    return app
