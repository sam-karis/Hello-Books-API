"""Hello Books models."""
from app import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """This class is a representation of users table."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password):
        """Initialize the users class."""
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_all(self):
        return User.query.all()

    def __repr__(self):
        return '<User: {}>'.format(self.email)

    @property
    def password(self):
        """Prevent the password from being accessed."""
        raise AttributeError('Password nod accessible')

    @password.setter
    def password(self, password):
        """Hash password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check password given is valid."""
        return check_password_hash(self.password, password)


class Books(db.Model):
    """This class is a representation of books table."""
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
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
