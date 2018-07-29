"""Create Hello Books API endpoints."""
import json
import re
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, jwt_required,
                                get_jwt_identity, get_raw_jwt)
# from app import app
from . import auth
from app.models import User, ActiveTokens, RevokedTokens
from app.decorators import admin_required
from app.email_token import generate_reset_password_token, confirm_reset_password_token, send_email

def validate_email(email):
    valid = re.match(
        "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip())
    if valid is None:
        return False
    return True


@auth.route('/api/v2/auth/register', methods=['POST'])
def register_user():
    """Endpoint for a new user to register."""
    name = request.json.get('name')
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')
    is_admin = request.json.get('is_admin')

    res = None
    if not password or len(password.strip()) < 6:
        res = {'Message': 'Fill in  a valid password to register'}
    if not email or not validate_email(email):
        res = {'Message': 'Fill in a valid email to register'}
    if not name or name.strip() == "":
        res = {'Message': 'Fill in  your name to register'}

    if res is not None:
        return jsonify(res), 406
    # Check the user with that email exist in the db.
    if not User.get_user_by_email(email):
        new_user = User(name=name, email=email.strip(), username=username)
        new_user.hash_password(password)
        if not new_user.check_password(confirm_password):
            return jsonify({'Message': 'Password do not match'}), 409
        if is_admin:
            new_user.is_admin = True
            new_user.save()
            response = jsonify(
                {'Message': 'Successfully registered as an Admin'}), 201
        else:
            new_user.save()
            response = jsonify(
                {'Message': 'Successfully registered as a User'}), 201
    else:
        response = jsonify(
            {'Message': 'Email already registered to another user'}), 409
    return response


@auth.route('/api/v2/auth/register', methods=['PUT', "GET"])
@jwt_required
@admin_required
def user_upgrade_view():
    """Upgrade a user into an admin and view all users."""
    if request.method == 'PUT':
        email = request.json.get('email')
        is_admin = request.json.get('is_admin')

        if not email or not validate_email(email):
            return jsonify({'Message': 'Fill in a valid email'})

        # Get user from db
        user = User.get_user_by_email(email)
        # check if password match
        if user:
            if type(is_admin) == bool:
                status = "Admin" if is_admin else "User"
                user.is_admin = is_admin
                user.save()
                response = jsonify(
                    {'Message': 'User of {} is now {}'.format(email, status)})
            else:
                response = jsonify(
                    {'Message': 'set a valid is_admin'})
        else:
            response = jsonify(
                {'Message': 'No user with registered with that email',
                 "status_code": 204})
        return response
    elif request.method == 'GET':
        return jsonify(users=[user.serialize for user in User.query.all()])


@auth.route('/api/v2/auth/login', methods=['POST'])
def user_login():
    """Endpoint for user to login."""
    email = request.json.get('email')
    password = request.json.get('password')
    if not email or not validate_email(email):
        return jsonify({"Message": "Enter a valid email"})
    if not password or password.strip() == "" or password is None:
        return jsonify({"Message": "Enter a valid password"})
    user = User.get_user_by_email(email)
    logged_in_user = ActiveTokens.find_user_with_token(email)
    if logged_in_user and not logged_in_user.is_expired() \
            and user.check_password(password):
        response = jsonify({'Message': 'You are already logged In',
                            'email': user.email, 'username': user.username,
                            "access_token": logged_in_user.access_token,
                            'is_admin': user.is_admin})
    elif logged_in_user and logged_in_user.is_expired() \
            and user.check_password(password):
        access_token = create_access_token(identity=email)
        logged_in_user.access_token = access_token
        logged_in_user.save_token()
        response = jsonify({'Message': 'Your token expired use token below.',
                            'access_token': access_token, 'email': user.email,
                            'username': user.username, 'is_admin': user.is_admin}), 200
    else:
        # Get the user from db using the mail
        if user and user.check_password(password):
            access_token = create_access_token(identity=email)
            ActiveTokens(email, access_token).save_token()
            response = jsonify({'Message': 'Successfuly login',
                                'access_token': access_token, 'email': user.email,
                                'username': user.username, 'is_admin': user.is_admin}), 200
        else:
            response = jsonify({'Message': 'Invalid email or password'}), 401
    return response


@auth.route('/api/v2/auth/logout', methods=['POST'])
@jwt_required
def user_logout():
    """Endpoint for user to logout."""
    email = request.json.get('email')
    if email is None or not validate_email(email):
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
    password = request.json.get('new_password')
    token = request.args.get('token')
    if not email or not validate_email(email):
        return jsonify({'Message': 'Enter email for user to reset password'})
    # Check if there is a user to with the email in db.
    updated_user = User.get_user_by_email(email)
    if not updated_user:
        res = jsonify({'Message': 'No user registered with {} as their email'
                       .format(email)})
    else:
        if token:
            token_email = confirm_reset_password_token(token)
            if token_email == updated_user.email:
                if not password or len(password.strip()) <= 6 or updated_user.check_password(password):
                    res = jsonify(
                        {'Message': 'Enter a valid new password'
                         '(must be more than 6 characters and not same as the old one)'})
                else:
                    updated_user.hash_password(password)
                    updated_user.save()
                    res = jsonify({'Message': 'Reset successful.'})
            else:
                res = jsonify(
                    {'Message': 'Invalid or expired token for the user.'})
        else:
            token = generate_reset_password_token(email)
            send_email(email, token)
            res = jsonify(
                {'Message': 'A password reset token has been sent to your email.'})

    return res
