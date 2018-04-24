import json
import os

from flask import jsonify, request

from . import book

from app.models import Books


@book.route('/api/v2/books', methods=['GET'])
def get_all_book():
    """Return all books."""
    BOOKS = Books.query.all()
    if not BOOKS:
        response = jsonify({"Message": "No books in the library"}), 204
    else:
        response = jsonify(books=[item.serialize for item in BOOKS]), 200
    return response


@book.route('/api/v2/books/<bookId>', methods=['GET'])
def get_specific_book_by_id(bookId):
    """Endpoint to interact with specific book."""
    try:
        bookId = int(bookId)

        # Get book with that id from db.
        book = Books.query.filter_by(book_id=bookId).first()
        # Check if such a book exist in db.
        if not book:
            return jsonify({'Message': 'No book with that Id.'})
        else:
            # Return the book in json format
            return jsonify(book.serialize)
    except ValueError:
        return jsonify({'Message': 'Use a valid book Id'}), 404
