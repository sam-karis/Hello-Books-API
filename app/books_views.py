"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request
from app import app
from .models import Users, Books
from .setup_data import BOOKS


@app.route('/api/v1/books', methods=['GET', 'POST'])
def all_book_handler():
    """Handle viewing of all books and adding a book."""
    if request.method == 'GET':
        return get_all_book()

    elif request.method == 'POST':
        return add_book()


def get_all_book():
    """Return all books."""
    return jsonify(books=[item.serialize for item in BOOKS])


def add_book():
    """Add books."""
    book_id = len(BOOKS) + 1
    # Get details of the book to be added
    title = request.json.get('title')
    author = request.json.get('author')
    description = request.json.get('description')
    edition = request.json.get('edition')

    if title is None:
        return jsonify({'Message': 'Give your book a title.'})
    if author is None:
        return jsonify({'Message': 'Give the author of the book'})
    if description is None or type(description) is int:
        return jsonify({'Message': 'Give your book a short description'})
    if edition is None:
        return jsonify({'Message': 'What is the edition of this book?'})

    book_added = Books(book_id, title, author, description, edition)

    # check if the book title exist.
    if book_added.title in [book.title for book in BOOKS]:
        return jsonify({'Message': 'A book with that title already exist.'})
    else:
        BOOKS.append(book_added)
        return jsonify({'Message': 'Book added successfully.'})


@app.route('/api/v1/books/<bookId>', methods=['GET', 'PUT', 'DELETE'])
def specific_book_handler(bookId):
    """Endpoint to interact with specific book."""
    if request.method == 'GET':

        return get_book(bookId)

    elif request.method == 'PUT':

        return modify_book(bookId)

    elif request.method == 'DELETE':
        return delete_book(bookId)


def get_book(bookId):
    """Get a book by Id."""
    bookId = int(bookId)
    for book in BOOKS:
        if book.book_id == bookId:
            return jsonify(book.serialize)
    return jsonify({'Message': 'No book with that Id.'})


def modify_book(bookId):
    """Update/modify a book by Id."""
    bookId = int(bookId)
    for book in BOOKS:
        if book.book_id == bookId:
            break
    if book is None:
        return ({'Message': 'No book with that Id.'})
    title = request.json.get('title')
    author = request.json.get('author')
    description = request.json.get('description')
    edition = request.json.get('edition')

    # check if the variable is to be updated
    try:
        if title:
            book.title = title
        if author:
            book.author = author
        if description:
            book.description = description
        if edition:
            book.edition = edition
    except:
        return jsonify({'Message': 'No update done.'})

    return jsonify({'Message': 'Your update is successful.'})


def delete_book(bookId):
    """Remove a book by Id."""
    if bookId in [None, ""] or not int(bookId):
        return jsonify({'Message': 'Enter a valid book id'})
    else:
        bookId = int(bookId)
        if bookId not in [book.book_id for book in BOOKS]:
            return jsonify({'Message': 'No book with that Id to delete.'})
        for book in BOOKS:
            if book.book_id == bookId:
                book_to_delete = book
                break
        if book_to_delete is not None:
            BOOKS.remove(book)
            return jsonify({'Message': "Book deleted successfully"})
