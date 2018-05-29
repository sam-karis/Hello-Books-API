"""Create Hello Books API endpoints."""
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from functools import wraps

from app.models import User, RevokedTokens


def admin_required(func):
    """Validate a user is admin and has a valid token."""

    @wraps(func)
    def verify_admin_and_token(*args, **kwargs):
        jti = get_raw_jwt()['jti']
        logged_user_email = get_jwt_identity()
        logged_user = User.get_user_by_email(logged_user_email)
        if RevokedTokens.is_jti_blacklisted(jti):
            return jsonify({'Message': 'The token has been blacklisted.'}), 401
        if not logged_user.is_admin:
            return jsonify({'Message': 'Need to be an admin add a continue.'}), 401
        return func(*args, **kwargs)
    return verify_admin_and_token
