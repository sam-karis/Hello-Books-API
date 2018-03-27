"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request
from app import app
from .models import Users, Books
from .setup_data import BOOKS


@app.route('/')
@app.route('/api/v1')
def hello():
    """Introduction to app."""
    return jsonify({'Message': 'WELCOME TO HELLO BOOKS'})


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
    # Get details of the book to be added
    book_id = request.args.get('book_id')
    title = request.args.get('title')
    author = request.args.get('author')
    description = request.args.get('description')
    edition = request.args.get('edition')
    pyear = request.args.get('pyear')
    quantity = request.args.get('quantity')

    if book_id in [None, ""]:
        return 'Enter book_id like {}'.format(len(BOOKS) + 1)
    else:
        book_id = int(book_id)

    if book_id in [book.book_id for book in BOOKS]:
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

    book_added = Books(book_id, title, author,
                       description, edition, pyear, quantity)

    # check if the book exist.
    if book_added in [book for book in BOOKS]:
        return 'A book with that title arleady exist.'
    else:
        BOOKS.append(book_added)
        return 'Book added successfully.'


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
    return 'No book with that Id.'


def modify_book(bookId):
    """Update/modify a book by Id."""
    bookId = int(bookId)
    for book in BOOKS:
        if book.book_id == bookId:
            break
    if book is None:
        return 'No book with that Id.'
    # get variable update
    book_id = request.args.get('book_id')
    title = request.args.get('title')
    author = request.args.get('author')
    description = request.args.get('description')
    edition = request.args.get('edition')
    pyear = request.args.get('pyear')
    quantity = request.args.get('quantity')

    # check if the variable is to be updated
    try:
        if book_id:
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


def delete_book(bookId):
    """Remove a book by Id."""
    bookId = int(bookId)
    for book in BOOKS:
        if book.book_id == bookId:
            book_to_delete = book
            break
    if book_to_delete is not None:
        BOOKS.remove(book)
        return "Book deleted successfully"
    return 'No book with that Id to delete.'
