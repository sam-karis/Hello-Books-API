
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
        return get_all_book_handler()

    elif request.method == 'POST':
        return add_book_handler()


def get_all_book_handler():
    """Get all books."""
    return jsonify(books=[item.serialize for item in BOOKS])


def add_book_handler():
    """Add books."""
    # Get details of the book to be added
    book_Id = request.args.get('book_Id')
    title = request.args.get('title')
    author = request.args.get('author')
    description = request.args.get('description')
    edition = request.args.get('edition')
    pyear = request.args.get('pyear')
    quantity = request.args.get('quantity')

    if book_Id is None:
        return 'Enter book_Id like {}'.format(len(BOOKS) + 1)
    else:
        book_Id = int(book_Id)

    if book_Id in [book.book_Id for book in BOOKS]:
        return 'The book_Id exists choose another one.'
    if title is None:
        return 'Give your book a title.'
    if author is None:
        return 'Give the author of the book'
    if description is None and type(description) is int:
        return 'Give your book a short description'
    if edition is None:
        return 'What is the edition of this book?'
    if pyear is None:
        return 'Give your book a pyear(Publish year)'
    if quantity is None:
        return 'What is the quantity of book/books you are adding?'

    bookadded = books(book_Id, title, author,
                      description, edition, pyear, quantity)

    # check if the book exist.
    if bookadded in [book for book in BOOKS]:
        return 'A book with that title arleady exist.'
    else:
        BOOKS.append(bookadded)
        return 'Book added successfully.'


@app.route('/api/v1/books/<bookId>', methods=['GET', 'PUT', 'DELETE'])
def specific_book_handler(bookId):
    """Endpoint to interact with specific book."""
    if request.method == 'GET':

        return get_book_handler(bookId)

    elif request.method == 'PUT':

        return modify_book_handler(bookId)

    elif request.method == 'DELETE':
        return delete_book_handler(bookId)


def get_book_handler(bookId):
    """Get a book by Id."""
    bookId = int(bookId)
    for book in BOOKS:
        if book.book_Id == bookId:
            return jsonify(book.serialize)
    return 'No book with that Id.'


def modify_book_handler(bookId):
    """Update/modify a book by Id."""
    bookId = int(bookId)
    for book in BOOKS:
        if book.book_Id == bookId:
            break
    if book is None:
        return 'No book with that Id.'
    # get variable update
    book_Id = request.args.get('book_Id')
    title = request.args.get('title')
    author = request.args.get('author')
    description = request.args.get('description')
    edition = request.args.get('edition')
    pyear = request.args.get('pyear')
    quantity = request.args.get('quantity')

    # check if the variable is to be updated
    try:
        if book_Id:
            return 'You cannot modify a Book Id'
        if title:
            book.title = title
        if author:
            book.author = author
        if description:
            book.description = description
        if edition:
            book.edition = edition
        if pyear:
            book.pyear = pyear
        if quantity:
            book.quantity = quantity
    except:
        pass

    return 'Your update is successful.'


def delete_book_handler(bookId):
    """Remove a book by Id."""
    bookId = int(bookId)
    for book in BOOKS:
        if book.book_Id == bookId:
            bookToDelete = book
            break
    if bookToDelete is not None:
        BOOKS.remove(book)
        return "Book deleted successfully"
    return 'No book with that Id to delete.'
