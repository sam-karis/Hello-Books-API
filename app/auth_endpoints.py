"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request
from app import app


@app.route('/api/v1/auth')
def auth_home():
    """Introduction to app."""
    return jsonify({'Message': 'WELCOME TO HELLO BOOKS'})


@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    """Endpoint for a new user to register."""
    return jsonify({'Message': 'User should register'})


@app.route('/api/v1/auth/login', methods=['POST'])
def user_login():
    """Endpoint for user to login."""
    return jsonify({'Message': 'User should log in'})


@app.route('/api/v1/auth/logout', methods=['POST'])
def user_logout():
    """Endpoint for user to logout."""
    return jsonify({'Message': 'User should logout'})


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def password_reset():
    """Endpoint for user to reset his/her password."""
    return jsonify({'Message': 'User should be able to reset password'})
