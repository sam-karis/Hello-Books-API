"""Create the app."""
import os
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
# local import
from config import app_config
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.secret_key = 'super secret key'
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'jwt-token-secret-key'

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .book import book as book_blueprint
    app.register_blueprint(book_blueprint)

    jwt = JWTManager(app)

    @app.errorhandler(404)
    def invalid_endpoint(error=None):
        """Handle wrong endpoints."""
        message = {
            'message': 'You entered an invalid url',
            'URL': 'Not found : ' + request.url
        }
        return jsonify(message), 404

    return app
