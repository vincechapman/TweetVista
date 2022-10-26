import os
from dotenv import load_dotenv
from app import create_app
from werkzeug.security import generate_password_hash
import models

load_dotenv()

tweet_vista = create_app()

# Removing old database instance
if os.path.exists("app/db.sqlite"):
    os.remove("app/db.sqlite")
    print("Old sqlite database has been deleted successfully")

# Creating database models
models.db.create_all(app=tweet_vista)
print("New database created!")

# Creating Super Admin if it doesn't already exist
with tweet_vista.app_context():

    if not models.User.query.get(1):
        new_user = models.User(
            email_address=os.environ['ADMIN_EMAIL'],
            password=generate_password_hash(os.environ['ADMIN_PASSWORD']),
            first_name=os.environ['ADMIN_FIRST_NAME'],
            last_name=os.environ['ADMIN_LAST_NAME'],
            role='Super Admin'
        )
        models.db.session.add(new_user)
        models.db.session.commit()

if __name__ == '__main__':
    tweet_vista.run()
