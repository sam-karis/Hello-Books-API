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

    if not name or name.strip() == "":
        return jsonify({'Message': 'Fill in  your name to register'})
    if not email or email.strip() == "":
        return jsonify({'Message': 'Fill in  your email to register'})
    if not password or password.strip() == "":
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

    if not email or email is None or email.strip() == "":
        return jsonify({"Message": "Enter a valid email"})
    if not password or password.strip() == "" or password is None:
        return jsonify({"Message": "Enter a valid password"})
    if email in [user.email for user in USERS]:
        if session.get(email):
            response = jsonify({'Message': 'You are already logged In'})
        else:
            for user in USERS:
                if user.email == email:
                    break
            if user.check_password(password):
                session[email] = True
                response = jsonify({'Message': 'Successfuly login'}), 200

            else:
                response = jsonify({'Messsage': 'Invalid email or password'})
        return response
    return jsonify({'Messsage': 'User with that email does not exist'}), 404


@app.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """Endpoint for user to logout."""
    email = request.json.get('email')
    if email is None:
        response = jsonify({
            "Message": "Enter the email of the user you want to logout."
        })
    else:
        if session.get(email):
            session[email] = False
            response = jsonify({'Message': 'Successfuly logged Out'})
        else:
            response = jsonify({'Message': 'User of {} is not logged In'
                                .format(email)})
    return response


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
