"""Create Hello Books API endpoints."""
import json

from flask import jsonify, request

from app import app

from .models import Books, Users
from .setup_data import BOOKS


@app.errorhandler(404)
def invalid_endpoint(error=None):
    """Handle wrong endpoints."""
    message = {
        'message': 'You entered an invalid url',
        'URL': 'Not found : ' + request.url
    }

    return jsonify(message), 404


@app.route('/api/v1/books', methods=['GET', 'POST'])
def all_book_handler():
    """Handle viewing of all books and adding a book."""
    if request.method == 'GET':
        return get_all_book()

    elif request.method == 'POST':
        return add_book()


def get_all_book():
    """Return all books."""
    response = [item.serialize for item in BOOKS]
    if len(response) == 0:
        response = {"Message": "No books in the library"}
        return jsonify(response), 204
    return jsonify(books=response), 200


def add_book():
    """Add books."""
    book_id = len(BOOKS) + 1
    # Get details of the book to be added
    title = request.json.get('title')
    author = request.json.get('author')
    description = request.json.get('description')
    edition = request.json.get('edition')

    def validate_book_details(book_element):
        """Check if book details entered are valid."""
        if book_element is None or book_element.strip() == "":
            return jsonify(
                {'Message': 'Give your book a {}.'.format(book_element)}
            )
    validate_book_details(title)
    validate_book_details(author)
    validate_book_details(description)
    validate_book_details(edition)
    book_added = Books(book_id, title, author, description, edition)
    # check if the book title exist.
    if book_added.title in [book.title for book in BOOKS]:
        return jsonify({'Message': 'A book with that title already exist.'})
    else:
        BOOKS.append(book_added)
        return jsonify({'Message': 'Book added successfully.'}), 201


@app.route('/api/v1/books/<bookId>', methods=['GET', 'PUT', 'DELETE'])
def specific_book_handler(bookId):
    """Endpoint to interact with specific book."""
    try:
        bookId = int(bookId)
        if request.method == 'GET':

            return get_book(bookId)

        elif request.method == 'PUT':

            return modify_book(bookId)

        elif request.method == 'DELETE':
            return delete_book(bookId)
    except ValueError:
        return jsonify({'Message': 'Use a valid book Id'}), 404


def get_book(bookId):
    """Get a book by Id."""
    for book in BOOKS:
        if book.book_id == bookId:
            return jsonify(book.serialize)
    return jsonify({'Message': 'No book with that Id.'})


def modify_book(bookId):
    """Update/modify a book by Id."""
    book_to_update = None
    for book in BOOKS:
        if book.book_id == bookId:
            book_to_update = book
            break
    if book_to_update is None:
        return ({'Message': 'No book with that Id.'})
    try:
        title = request.json.get('title')
        if title and title.strip() != "":
            if title in [book.title for book in BOOKS]:
                return jsonify({'Message': 'Book with that title exists.'})
            book.title = title

        def validate_update(element_to_update):
            """Validate element before update."""
            element_to_update = request.json.get(element_to_update)
            if element_to_update and element_to_update.strip() != "":
                book.element_to_update = element_to_update
        validate_update('author')
        validate_update('description')
        validate_update('edition')
    except AttributeError:
        pass
    return jsonify({'Message': 'Your update is successful.'})


def delete_book(bookId):
    """Remove a book by Id."""
    if bookId not in [book.book_id for book in BOOKS]:
        return jsonify({'Message': 'No book with that Id to delete.'})
    for book in BOOKS:
        if book.book_id == bookId:
            book_to_delete = book
            break
    if book_to_delete is not None:
        BOOKS.remove(book)
        return jsonify({'Message': "Book deleted successfully"})
