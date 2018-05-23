"""Create Hello Books API endpoints."""
import json
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, get_raw_jwt, jwt_required
# Local imports
from app.models import BookHistory, Books, RevokedTokens, User
from . import user


@user.route('/api/v2/users/books', methods=['GET'])
@jwt_required
def get_user_borrow_history():
    email = get_jwt_identity()
    returned = request.args.get('returned')
    if returned and returned == "false":
        books_not_returned = BookHistory.get_books_not_returned(email)
        if not books_not_returned:
            response = jsonify(
                {"Message": "You do not have a book that is not returned."})
        else:
            response = jsonify(
                History=[{**log.serialize, **log.book.serialize_history}
                         for log in books_not_returned]
            )
    else:
        books_borrowed = BookHistory.get_user_history(email)
        if not books_borrowed:
            response = jsonify(
                {"Message": "You do not have a borrowing history."})
        else:
            response = jsonify(
                books=[{**borrow.serialize, **borrow.book.serialize_history}
                       for borrow in books_borrowed]
            )
    return response


@user.route('/api/v2/users/books/<bookId>', methods=['POST', 'PUT'])
@jwt_required
def borrow(bookId):
    """Endpoint for borrowing a book."""
    try:
        bookId = int(bookId)
    except ValueError:
        return jsonify({"Message": "Use a valid books Id"})
    email = request.json.get('email')
    if not email or email.strip() == "":
        response = jsonify({"Message": "Enter your email to continue"})
    else:
        jti = get_raw_jwt()['jti']
        logged_user = get_jwt_identity()
        if logged_user != email or RevokedTokens.is_jti_blacklisted(jti):
            response = jsonify(
                {"Message": "Login to get a valid token to Continue"})
        else:
            book = Books.get_book_by_id(bookId)
            if not book:
                response = jsonify({"Message": "No book with that Id."})
            else:
                if request.method == "POST":
                    if book.status == "Borrowed":
                        return jsonify({
                            "Message": "Somebody already borrowed this book"})
                    user = User.get_user_by_email(email)
                    return_date = datetime.now() + timedelta(days=7)
                    book_borrowed = BookHistory(user_email=user.email,
                                                book_id=book.book_id,
                                                return_date=return_date)

                    response = jsonify(
                        {**{"Message": "Book borrowed successfully"}, **book.serialize_history,
                         **book_borrowed.serialize})

                    book_borrowed.save_book()
                    # update books status in library
                    book.status = "Borrowed"
                    book.save_book()

                elif request.method == "PUT":
                    book_returned = BookHistory.get_book_by_id(bookId)
                    if book.status == "Available":
                        return jsonify({
                            "Message": "The book is not borrowed to return"})
                    # Set book status to available in book db.
                    book.status = "Available"
                    book.save_book()
                    # Set book status & return date in BookHistory db.
                    book_returned.returned = True
                    book_returned.return_date = datetime.now()
                    book_returned.save_book()
                    response = jsonify(
                        {**{"Message": "Book returned successfully"}, **book.serialize_history,
                         **book_returned.serialize})
    return response
