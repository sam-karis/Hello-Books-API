"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_identity, get_raw_jwt)
# from app import app
from . import auth
from app.models import User, ActiveTokens, RevokedTokens


@auth.route('/api/v2/auth/register', methods=['POST'])
def register_user():
    """Endpoint for a new user to register."""
    USERS = User.query.all()
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    is_admin = request.json.get('is_admin')

    if not name or name.strip() == "":
        return jsonify({'Message': 'Fill in  your name to register'})
    if not email or email.strip() == "":
        return jsonify({'Message': 'Fill in  your email to register'})
    if not password or password.strip() == "":
        return jsonify({'Message': 'Fill in  your password to register'})

    # Check the user with that email exist in the db.
    if not User.get_user_by_email(email):
        new_user = User(name=name, email=email)
        new_user.hash_password(password)
        if is_admin or is_admin.lower() == 'true':
            new_user.is_admin = True
            new_user.save()
            response = jsonify(
                {'Message': 'Successfully registered as a Admin'}), 201
        else:
            new_user.save()
            response = jsonify(
                {'Message': 'Successfully registered as a User'}), 201
    else:
        response = jsonify(
            {'Message': 'Email already registered to another user'})
    return response


@auth.route('/api/v2/auth/login', methods=['POST'])
def user_login():
    """Endpoint for user to login."""
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or email is None or email.strip() == "":
        return jsonify({"Message": "Enter a valid email"})
    if not password or password.strip() == "" or password is None:
        return jsonify({"Message": "Enter a valid password"})
    logged_in_user = ActiveTokens.find_user_with_token(email)
    if logged_in_user and not logged_in_user.is_expired():
        response = jsonify({'Message': 'You are already logged In',
                            "access_token": logged_in_user.access_token})
    elif logged_in_user and logged_in_user.is_expired():
        access_token = create_access_token(identity=email)
        logged_in_user.access_token = access_token
        logged_in_user.save_token()
        response = jsonify({'Message': 'Your token expired use token below.',
                            'token': access_token}), 200
    else:
        # Get the user from db using the mail
        user = User.get_user_by_email(email)
        if user and user.check_password(password):
            access_token = create_access_token(identity=email)
            ActiveTokens(email, access_token).save_token()
            response = jsonify({'Message': 'Successfuly login',
                                'token': access_token}), 200
        else:
            response = jsonify({'Messsage': 'Invalid email or password'}), 401
    return response


@auth.route('/api/v2/auth/logout', methods=['POST'])
@jwt_required
def user_logout():
    """Endpoint for user to logout."""
    email = request.json.get('email')
    if email is None:
        response = jsonify({
            "Message": "Enter the email of the user you want to logout."
        })
    else:
        jti = get_raw_jwt()['jti']
        logged_user = get_jwt_identity()
        if logged_user == email and not RevokedTokens.is_jti_blacklisted(jti):
            token_to_revoke = RevokedTokens(jti=jti)
            token_to_revoke.revoke()
            ActiveTokens.find_user_with_token(email).delete_active_token()
            response = jsonify({'Message': 'Successfuly logged Out'})
        else:
            response = jsonify(
                {'Message': '{} is not logged In or token has been blacklisted'
                 .format(email)})
    return response


@auth.route('/api/v2/auth/reset-password', methods=['POST'])
def password_reset():
    """Endpoint for user to reset his/her password."""
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or email.strip() == "":
        return jsonify({'Message': 'Enter email for user to reset password'})
    # Check if there is a user to with the email in db.
    updated_user = User.get_user_by_email(email)
    if not updated_user:
        return jsonify({'Message': 'No user registered with {} as their email'
                        .format(email)})
    else:
        if not password or password.strip() == "":
            return jsonify({'Message': 'Enter your new password'})
        elif updated_user.check_password(password):
            return jsonify({'Message': 'Current password used thus no reset.'})
        else:
            updated_user.hash_password(password)
            updated_user.save()
            return jsonify({'Message': 'Reset successful.'})
