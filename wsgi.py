from app import create_app, models

tweet_vista = create_app()
models.db.create_all(app=tweet_vista)

if __name__ == '__main__':
    tweet_vista.run()
