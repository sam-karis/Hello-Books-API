"""Create Hello Books API endpoints."""
import json
import os

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt

from . import admin
from app.models import Books, User, RevokedTokens
from app.decorators import admin_required


@admin.route('/api/v2/books', methods=['POST'])
@jwt_required
@admin_required
def add_book():

    # Get details of the book to be added
    title = request.json.get('title')
    author = request.json.get('author')
    description = request.json.get('description')
    edition = request.json.get('edition')

    res = None
    if title is None or title.strip() == "":
        res = {'Message': 'Give your book a title.'}
    if author is None or author.strip() == "":
        res = {'Message': 'Give the author of the book'}
    if description is None or description.strip() == "":
        res = {'Message': 'Give your book a short description'}
    if edition is None or edition.strip() == "":
        res = {'Message': 'What is the edition of this book?'}
    if res is not None:
        return jsonify(res)

    book_added = Books(title=title,
                       author=author,
                       description=description,
                       edition=edition)

    # check if the book title exist.
    if Books.query.filter_by(title=title).first():
        response = jsonify(
            {'Message': 'A book with that title already exist.'}), 409
    else:
        book_added.save_book()
        response = jsonify({'Message': 'Book added successfully.'}), 201
    return response


@admin.route('/api/v2/books/<bookId>', methods=['PUT', 'DELETE'])
@jwt_required
@admin_required
def specific_book_handler(bookId):
    """Endpoint to interact with specific book by id."""

    try:
        bookId = int(bookId)
        # Get book with that id from db.
        book = Books.query.filter_by(book_id=bookId).first()
        # Check if such a book exist in db.
        if not book:
            return jsonify({'Message': 'No book with that Id.', 'status_code': 204})
        elif request.method == 'PUT':
            """Update/modify a book by Id."""
            title = str(request.json.get('title', ''))
            author = str(request.json.get('author', ''))
            description = str(request.json.get('description', ''))
            edition = str(request.json.get('edition', ''))
            # check if the variable is to be updated
            try:
                if title and title.strip() != "":
                    book.title = title
                if author and author.strip() != "":
                    book.author = author
                if description and description.strip() != "":
                    book.description = description
                if edition and edition.strip() != "":
                    book.edition = edition
            except:
                pass
            book.save_book()
            return jsonify({'Message': 'Your update is successful.'}), 200

        elif request.method == 'DELETE':
            book.delete_book()
            return jsonify({'Message': "Book deleted successfully"}), 200
    except ValueError:
        return jsonify({'Message': 'Use a valid book Id'}), 404
