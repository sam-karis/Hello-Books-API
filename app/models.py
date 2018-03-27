"""Hello Books models."""
from werkzeug.security import check_password_hash, generate_password_hash


class Person(object):
    """Common class for admin and user."""

    def __init__(self, name, email, password):
        """Initialize the users class."""
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)


class Users(Person):
    """Users model."""

    def __init__(self, user_id, name, email, password):
        """Initialize the users class."""
        self.user_id = user_id
        Person.__init__(self, name, email, password)

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
        self, book_id, title, author, description, edition, pyear, quantity
    ):
        """Initialize the model."""
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.edition = edition
        self.pyear = pyear
        self.quantity = quantity

    @property
    def serialize(self):
        """Serialize."""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'edition': self.edition,
            'pyear': self.pyear,
            'quantity': self.quantity
        }


class BookHistory(object):
    """books model to record return and borrowing of a book."""

    def __init__(self, book_id, user_id, dateBorrowed, dateReturned, status):
        """Initialize the model."""
        self.book_id = book_id
        self.user_id = user_id
        self.dateBorrowed = dateBorrowed
        self.dateReturned = dateReturned
        self.status = status

    @property
    def serialize(self):
        """Serialize bookHistory."""
        return {
            'book_id': self.book_id,
            'user_id': self.user_id,
            'dateBorrowed': self.dateBorrowed,
            'dateReturned': self.dateReturned,
            'status': self.status
        }
