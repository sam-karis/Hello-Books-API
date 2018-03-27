"""Hello Books models."""


class person(object):
    """Common class for admin and user."""

    def __init__(self, name, email, password):
        """Initialize the users class."""
        self.name = name
        self.email = email
        self.password = password


class users(person):
    """Users model."""

    def __init__(self, user_Id, name, email, password):
        """Initialize the users class."""
        self.user_Id = user_Id
        person.__init__(self, name, email, password)

    @property
    def serialize(self):
        """Serialize user Id."""
        return {
            'user_Id': self.user_Id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }


class admin(person):
    """Admin model."""

    def __init__(self, admin_Id, name, email, password):
        """Initialize the admin model."""
        self.admin_Id = admin_Id
        person.__init__(self, name, email, password)

    @property
    def serialize(self):
        """Serialize admin Id."""
        return {
            'admin_Id': self.admin_Id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }


class books(object):
    """books models."""

    def __init__(
        self, book_Id, title, author, description, edition, pyear, quantity
    ):
        """Initialize the model."""
        self.book_Id = book_Id
        self.title = title
        self.author = author
        self.description = description
        self.edition = edition
        self.pyear = pyear
        self.quantity = quantity

    @property
    def serialize(self):
        return {
            'book_Id': self.book_Id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'edition': self.edition,
            'pyear': self.pyear,
            'quantity': self.quantity
        }


class bookHistory(object):
    """books model to record return and borrowing of a book."""

    def __init__(self, book_Id, user_Id, dateBorrowed, dateReturned, status):
        """Initialize the model."""
        self.book_Id = book_Id
        self.user_Id = user_Id
        self.dateBorrowed = dateBorrowed
        self.dateReturned = dateReturned
        self.status = status

    @property
    def serialize(self):
        """Serialize bookHistory."""
        return {
            'book_Id': self.book_Id,
            'user_Id': self.user_Id,
            'dateBorrowed': self.dateBorrowed,
            'dateReturned': self.dateReturned,
            'status': self.status
        }
