"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request
from app import app
from app.models import Users
from app.setup_data import USERS


@app.route('/api/v1/auth')
def auth_home():
    """Introduction to app."""
    return jsonify({'Message': 'WELCOME TO HELLO BOOKS'})


@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    """Endpoint for a new user to register."""
    user_id = request.args.get('user_id')
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')

    if email not in [user.email for user in USERS]:
        new_user = Users(user_id, name, email, password)
        new_user.hash_password(password)
        USERS.append(new_user)

        response = jsonify({'Message': 'User has successfully registered'})
        response.status_code = 201
        return response
    else:
        response = jsonify({'Message': 'User already registered'})
        response.status_code = 202
        return response


@app.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """Endpoint for user to login."""
    email = request.args.get('email')
    password = request.args.get('password')

    if email in [user.email for user in USERS]:
        for user in USERS:
            if user.email is email:
                break
        if user.check_password(password):
            return jsonify({'Message': 'Successfuly login'}), 200
        else:
            response = jsonify({'Messsage': 'Invalid email or password'})
            response.status_code = 401
            return response
    return jsonify({'Messsage': 'User with that email does not exist'}), 404



@app.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """Endpoint for user to logout."""
    return jsonify({'Message': 'User should logout'})


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def password_reset():
    """Endpoint for user to reset his/her password."""
    return jsonify({'Message': 'User should be able to reset password'})
