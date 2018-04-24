"""Create Hello Books API endpoints."""
import json
import os

from flask import jsonify, request

from app import app

from app.models import Books


@app.route('/api/v2/books', methods=['GET', 'POST'])
def all_book_handler():
    """Handle viewing of all books and adding a book."""
    if request.method == 'GET':
        return get_all_book()

    elif request.method == 'POST':
        return add_book()


def get_all_book():
    """Return all books."""
    BOOKS = Books.query.all()
    return jsonify(books=[item.serialize for item in BOOKS])


def add_book():
    """Add books."""
    BOOKS = Books.query.all()

    # Get details of the book to be added
    title = request.json.get('title')
    author = request.json.get('author')
    description = request.json.get('description')
    edition = request.json.get('edition')

    if title is None or title.strip() == "":
        return jsonify({'Message': 'Give your book a title.'})
    if author is None or author.strip() == "":
        return jsonify({'Message': 'Give the author of the book'})
    if description is None or description.strip() == "" or type(description) is int:
        return jsonify({'Message': 'Give your book a short description'})
    if edition is None or edition.strip() == "":
        return jsonify({'Message': 'What is the edition of this book?'})

    book_added = Books(title=title,
                       author=author,
                       description=description,
                       edition=edition)

    # check if the book title exist.
    if book_added.title in [book.title for book in BOOKS]:
        return jsonify({'Message': 'A book with that title already exist.'})
    else:
        book_added.save_book()
        return jsonify({'Message': 'Book added successfully.'})


@app.route('/api/v2/books/<int:bookId>', methods=['GET', 'PUT', 'DELETE'])
def specific_book_handler(bookId):
    """Endpoint to interact with specific book."""

    """Get book with that id from db."""
    book = Books.query.filter_by(book_id=bookId).first()

    """Check if such a book exist in db."""
    if not book:
        return jsonify({'Message': 'No book with that Id.'})

    elif request.method == 'GET':
        """Get a book by Id."""
        return jsonify(book.serialize)

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
        return jsonify({'Message': 'Your update is successful.'})

    elif request.method == 'DELETE':
        book.delete_book()
        return jsonify({'Message': "Book deleted successfully"})


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
