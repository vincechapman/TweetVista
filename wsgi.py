from app import create_app, models

twitter_vista = create_app()
models.db.create_all(app=twitter_vista)

if __name__ == '__main__':
    twitter_vista.run()
