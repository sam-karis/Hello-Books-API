"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request
from app import app
from .models import users


@app.route('/')
def hello():
    """Introduction to app."""
    return "WELCOME TO HELLO BOOKS"


@app.route('/api/v1/books', methods=['POST', 'PUT'])
def addBook():
    """add books to app."""
    if request.method == 'POST':
        return "It is a post request"
    return "Not a post method"
