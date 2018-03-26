
"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request
from app import app
from .models import admin, users, books, bookHistory
from .setup_data import BOOKS, USERS, ADMIN


@app.route('/')
def hello():
    """Introduction to app."""
    return "WELCOME TO HELLO BOOKS!"


@app.route('/api/v1/books', methods=['GET', 'POST'])
def all_book_handler():
    """Handle books access."""
    if request.method == 'GET':
        """Gets all books."""
        return jsonify(books=[item.serialize for item in BOOKS])

    elif request.method == 'POST':
        """Add books."""
        title = request.args.get('title')
        author = request.args.get('author')
        description = request.args.get('description')
        edition = request.args.get('edition')
        pyear = request.args.get('pyear')
        quantity = request.args.get('quantity')
        if title is None:
            return 'Give your book a title.'
        elif author is None:
            return 'Give the author of the book'
        elif description is None and type(description) is int:
            return 'Give your book a short description'
        elif edition is None:
            return 'What is the edition of this book?'
        elif pyear is None:
            return 'Give your book a pyear(Publish year)'
        elif quantity is None:
            return 'What is the quantity of book/books you are adding?'
        bookadded = books(title, author, description, edition, pyear, quantity)
        # check if the book exist.
        if bookadded.title in [book.title for book in BOOKS]:
            return 'A book with that title arleady exist.'
        else:
            BOOKS.append(bookadded)
            return 'Book added successfully.'


@app.route('/api/v1/books/<bookId>', methods=['GET', 'PUT', 'DELETE'])
def specific_book_handler(bookId):
    """Should retrive a book."""
    if request.method == 'GET':
        bookId = int(bookId) - 1
        if bookId > len(BOOKS) or bookId < 0:
            return 'Book Id does Not exist. The id range from {} to {}' .format(1, len(BOOKS))
        return jsonify(book=BOOKS[bookId].serialize)

    elif request.method == 'PUT':
        return 'Should update a book'
    elif request.method == 'DELETE':
        return "Should remove a book."
