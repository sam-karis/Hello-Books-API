"""Create Hello Books API endpoints."""
import json
from flask import jsonify, request, session
from datetime import datetime
from datetime import timedelta
from app import app
from .models import Users, Books, BookHistory
from .setup_data import BOOKS, USERS, BOOKHISTORY


@app.route('/api/v1/users/books/<bookId>', methods=['POST'])
def borrow(bookId):
    """Endpoint for borrowing a book."""
    bookId = int(bookId)
    email = request.json.get('email')
    return_date = datetime.now() + timedelta(days=7)
    if email is None:
        return jsonify({"Message": "Enter your email to borrow a book"})
    else:
        if not session.get(email):
            return jsonify({"Message": "Login to borrow a book"})
        else:
            if bookId not in [book.book_id for book in BOOKS]:
                response = jsonify({"Message": "No book with that Id."})
            else:
                for book in BOOKS:
                    if book.book_id == bookId:
                        if book.status == "Borrowed":
                            return jsonify({"Message": "The Book is already borrowed"})
                            break
                        book.status = "Borrowed"
                        break
                for user in USERS:
                    if user.email == email:
                        break
                book_borrowed = BookHistory(
                    book.book_id, book.title, user.name, return_date)
                BOOKHISTORY.append(book_borrowed)

                response = jsonify({**{"Message": "Book borrowed successfully"},
                                    **book_borrowed.serialize})
            return response
