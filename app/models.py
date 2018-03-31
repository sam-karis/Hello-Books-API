"""Hello Books models."""
from werkzeug.security import check_password_hash, generate_password_hash


class Person(object):
    """Common class for admin and user."""

    def __init__(self, name, email, password):
        """Initialize the users class."""
        self.name = name
        self.email = email
        self.password = password


class Users(Person):
    """Users model."""

    def __init__(self, user_id, name, email, password):
        """Initialize the users class."""
        self.user_id = user_id
        Person.__init__(self, name, email, password)

    def hash_password(self, password):
        """Hash password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check password given is valid."""
        return check_password_hash(self.password, password)

    @property
    def serialize(self):
        """Serialize user Id."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }


class Admin(Person):
    """Admin model."""

    def __init__(self, admin_id, name, email, password):
        """Initialize the admin model."""
        self.admin_id = admin_id
        Person.__init__(self, name, email, password)

    @property
    def serialize(self):
        """Serialize admin Id."""
        return {
            'admin_Id': self.admin_id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }


class Books(object):
    """books models."""

    def __init__(
        self, book_id, title, author, description, edition, status="Available"
    ):
        """Initialize the model."""
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.edition = edition
        self.status = status

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


class BookHistory(object):
    """books model to record return and borrowing of a book."""

    def __init__(self, book_id, book_title,
                 user_name, return_date, status="Not returned"):
        """Initialize the model."""
        self.book_id = book_id
        self.book_title = book_title
        self.user_name = user_name
        self.return_date = return_date
        self.status = status

    @property
    def serialize(self):
        """Serialize bookHistory."""
        return {
            "book_id": self.book_id,
            'book_title': self.book_title,
            'user_name': self.user_name,
            'return_date': self.return_date,
            'status': self.status
        }
