"""Hello Books models."""


class users(object):
    """Users model."""

    def __init__(self, user_id, username, email, password):
        """Initialize the users class."""
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }


class admin(object):
    """Admin model."""

    def __init__(self, admin_id, adminname, email, password):
        """Initialize the admin model."""
        self.admin_id = admin_id
        self.adminname = adminname
        self.email = email
        self.password = password

    @property
    def serialize(self):
        return {
            'admin_id': self.admin_id,
            'adminname': self.adminname,
            'email': self.email,
            'password': self.password
        }


class books(object):
    """books models."""

    def __init__(self, title, author, description, edition, pyear, quantity):
        """Initialize the model."""
        self.title = title
        self.author = author
        self.description = description
        self.edition = edition
        self.pyear = pyear
        self.quantity = quantity
    
    @property
    def serialize(self):
        return {
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'edition': self.edition,
            'pyear': self.pyear,
            'quantity': self.quantity
        }


class bookHistory(object):
    """books model to record return and borrowing of a book."""

    def __init__(self, title, user_id, dateBorrowed, dateReturned, status):
        """Initialize the model."""
        self.title = title
        self.user_id = user_id
        self.dateBorrowed = dateBorrowed
        self.dateReturned = dateReturned
        self.status = status

    @property
    def serialize(self):
        return {
            'title': self.title,
            'user_id': self.user_id,
            'dateBorrowed': self.dateBorrowed,
            'dateReturned': self.dateReturned,
            'status': self.status
        }