import os
from dotenv import load_dotenv
from app import create_app, models

load_dotenv()

tweet_vista = create_app()
models.db.create_all(app=tweet_vista)

# Creating Super Admin if it doesn't already exist
with tweet_vista.app_context():
    if not models.User.query.get(1):
        new_user = models.User(
            email=os.environ['ADMIN_EMAIL'],
            password=os.environ['ADMIN_PASSWORD'],
            name=os.environ['ADMIN_NAME'],
            role='super_admin'
        )
        models.db.session.add(new_user)
        models.db.session.commit()

if __name__ == '__main__':
    tweet_vista.run()
