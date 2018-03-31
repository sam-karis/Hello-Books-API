"""Create the app."""
from flask import Flask
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'super secret key'
# local import
from config import app_config


def create_app(config_name):
    """Create the app."""
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app


from app import books_views, auth_views, users_views
