"""Hello Books models."""


class users(object):
    """Users model."""

    def __init__(self, user_id, username, email, password):
        """Initialize the users class."""
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password


class admin(object):
    """Admin model."""

    def __init__(self, admin_id, adminname, email, password):
        """Initialize the admin model."""
        self.admin_id = admin_id
        self.adminname = adminname
        self.email = email
        self.password = password


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


class bookHistory(object):
    """books model to record return and borrowing of a book."""

    def __init__(self, title, user_id, dateBorrowed, dateReturned, status):
        """Initialize the model."""
        self.title = title
        self.user_id = user_id
        self.dateBorrowed = dateBorrowed
        self.dateReturned = dateReturned
        self.status = status
