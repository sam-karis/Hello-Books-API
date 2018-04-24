"""Hello Books models."""
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta


class User(db.Model):
    """This class is a representation of users table."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all(self):
        return User.query.all()

    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return '<User: {}>'.format(self.email)

    def hash_password(self, password):
        """Hash password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password given is valid."""
        return check_password_hash(self.password_hash, password)


class Books(db.Model):
    """This class is a representation of books table."""
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, unique=True)
    author = db.Column(db.String(60))
    description = db.Column(db.String(200))
    edition = db.Column(db.String(20))
    status = db.Column(db.String(20), default="Available")

    def __init__(
        self, title, author, description, edition, status="Available"
    ):
        """Initialize the model."""
        self.title = title
        self.author = author
        self.description = description
        self.edition = edition
        self.status = status

    def save_book(self):
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        db.session.delete(self)
        db.session.commit()

    def get_book_by_id(book_id):
        return Books.query.filter_by(book_id=book_id).first()

    def __repr__(self):
        return '<Book: {}>'.format(self.book_id)

    @property
    def serialize(self):
        """Serialize."""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'edition': self.edition,
            'status': self.status
        }


class BookHistory(db.Model):
    """This class is a representation of books borrowing table."""
    __tablename__ = 'booksHistory'

    log_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    time_borrowed = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_email = db.Column(db.String(60))
    title = db.Column(db.String(60))
    user_name = db.Column(db.String(60))
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="Not returned")

    def get_user_history(email):
        return BookHistory.query.filter_by(user_email=email).all()

    def get_book_by_id(book_id):
        return BookHistory.query.filter_by(
            book_id=book_id, status='Not returned').first()

    def save_book(self):
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):
        """Serialize bookHistory."""
        return {
            "user_name": self.user_email,
            "book_id": self.book_id,
            'time_borrowed': self.time_borrowed,
            'book_title': self.title,
            'user_name': self.user_name,
            'return_date': self.return_date,
            'status': self.status
        }


class RevokedTokens(db.Model):
    """This class is a representation of tokens issued table."""
    __tablename__ = 'revoked_tokens'

    token_id = db.Column(db.Integer, primary_key=True)
    time_revoked = db.Column(db.DateTime, default=db.func.current_timestamp())
    jti = db.Column(db.String(200), unique=True)

    def revoke(self):
        db.session.add(self)
        db.session.commit()

    def is_jti_blacklisted(jti):
        query = RevokedTokens.query.filter_by(jti=jti).first()
        if query:
            return True
        return False


class ActiveTokens(db.Model):
    """This class is a representation of tokens issued table."""
    __tablename__ = 'active_tokens'

    token_id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_email = db.Column(db.String, unique=True)
    access_token = db.Column(db.String, unique=True)

    def __init__(self, user_email, access_token):
        self.user_email = user_email
        self.access_token = access_token

    def save_token(self):
        db.session.add(self)
        db.session.commit()

    def delete_active_token(self):
        db.session.delete(self)
        db.session.commit()

    def is_expired(self):
        return (datetime.now() - self.time_created) > timedelta(minutes=15)

    def find_user_with_token(user_email):
        return ActiveTokens.query.filter_by(user_email=user_email).first()
