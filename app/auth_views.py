"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request, session
from app import app
from app.models import Users
from app.setup_data import USERS


@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    """Endpoint for a new user to register."""
    user_id = len(USERS) + 1
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    if not name:
        return jsonify({'Message': 'Fill in  your name to register'})
    if not email:
        return jsonify({'Message': 'Fill in  your email to register'})
    if not password:
        return jsonify({'Message': 'Fill in  your password to register'})

    if email not in [user.email for user in USERS]:
        new_user = Users(user_id, name, email, password)
        new_user.hash_password(password)
        USERS.append(new_user)

        return jsonify({'Message': 'User has successfully registered'})
    else:
        return jsonify({'Message': 'User already registered'})


@app.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """Endpoint for user to login."""
    email = request.json.get('email')
    password = request.json.get('password')

    if email in [user.email for user in USERS]:
        for user in USERS:
            if user.email == email:
                break
        if user.check_password(password):
            session['logged_in'] = True
            return jsonify({'Message': 'Successfuly login'}), 200

        else:
            response = jsonify({'Messsage': 'Invalid email or password'})
            response.status_code = 401
            # return response
            return jsonify(user.serialize)
    return jsonify({'Messsage': 'User with that email does not exist'}), 404


@app.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """Endpoint for user to logout."""
    if session['logged_in']:
        session['logged_in'] = False
        return jsonify({'Message': 'Successfuly logged Out'})
    else:
        return jsonify({'Message': 'You are not logged In'})


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def password_reset():
    """Endpoint for user to reset his/her password."""
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None:
        return jsonify({'Message': 'Enter your email and the new password'})
    for user in USERS:
        if user.email == email:
            updated_user = user
            USERS.remove(user)
            break
    if updated_user is None:
        return jsonify({'Message': 'User does not exist'})
    else:
        if password in ["", None]:
            jsonify({'Message': 'Enter your new password'})
        else:
            updated_user.hash_password(password)
            USERS.append(updated_user)
            return jsonify({'Message': 'Reset successful.'})
