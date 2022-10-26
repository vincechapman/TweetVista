from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    # Account details
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profile_image = db.Column(db.String(150))
    role = db.Column(db.String(100), nullable=False, default='Super Admin')

    # Twitter details
    twitter_handle = db.Column(db.Text)
    twitter_screen_name = db.Column(db.Text)
    twitter_profile_image = db.Column(db.Text)

    # Account setup
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    twitter_connected = db.Column(db.Boolean, nullable=False, default=False)
    business_information_provided = db.Column(db.Boolean, nullable=False, default=False)
    onboarded = db.Column(db.Boolean, nullable=False, default=False)

    # Business details
    company_name = db.Column(db.String(100))
    company_size = db.Column(db.Integer)
    role_in_company = db.Column(db.String(100))

    def __repr__(self):
        return self.name


class Campaigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_live = db.Column(db.Boolean, nullable=False, default=False)
    filters = db.Column(db.Text)  # A list of client-side filters
