from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Test(db.Model):
    number = db.Column(db.Integer, primary_key=True)
