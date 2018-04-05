"""Create the app."""
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# local import
from config import app_config
db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[os.getenv('FLASK_CONFIG')])
app.config.from_pyfile('config.py')
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from . import books_views, auth_views, users_views
