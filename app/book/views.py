import json
from flask import jsonify, request
from flask_paginate import Pagination

# Local imports
from . import book
from app.models import Books


@book.route('/api/v2/books', methods=['GET'])
def get_all_book():
    """Return all books."""
    books_in_library = Books.query.count()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', books_in_library, type=int)

    BOOKS = Books.query.order_by(Books.book_id).paginate(
        per_page=int(limit), page=int(page), error_out=False)

    if not BOOKS.items:
        response = jsonify({"Message": "No books on this page.",
                            "Number of Pages": BOOKS.pages,
                            "status_code": 204})
    else:
        info = {"Total pages": BOOKS.pages,
                "books per page": BOOKS.per_page,
                "current page": BOOKS.page,
                "next page": BOOKS.next_num,
                "prev page": BOOKS.prev_num}
        response = jsonify(General_information= info, books=[item.serialize for item in BOOKS.items])
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
            return jsonify({'Message': 'No book with that Id.', 'status': 204})
        else:
            # Return the book in json format
            return jsonify(book.serialize), 200
    except ValueError:
        return jsonify({'Message': 'Use a valid book Id'}), 404
