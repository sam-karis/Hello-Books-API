"""Unittest for API book endpoints."""
import unittest
import json
# local imports.
from app import create_app, db
from app.models import Books
from .test_admin import TestAdminEndpoints


class TestUserEndpoints(unittest.TestCase):
    """Test users endpoints."""

    def setUp(self):
        """Initialize and define variables for testing."""
        config_name = 'testing'
        self.app = create_app(config_name)
        self.client = self.app.test_client()

        # New book
        self.book = {
            "author": "Sam",
            "description": "Intro to data science using python",
            "edition": "4TH",
            "title": "Data science for Dummies"
        }

        # A second book
        self.book_two = {
            "author": "Peris",
            "description": "Basic of living a successful life",
            "edition": "5TH",
            "title": "Winning start in your mind"
        }

        # Admin sample details to register new admin
        self.admin = {"name": "sam",
                      "email": "samkaris@andela.com",
                      "password": "adminsecretpass",
                      "confirm_password": "adminsecretpass",
                      "is_admin": True}

        # Admin sample details to login
        self.admin_login = {"email": "samkaris@andela.com",
                            "password": "adminsecretpass"}

        # User sample details to register new user
        self.user = {"name": "Peris",
                     "email": "peris@andela.com",
                     "password": "usersecretpass",
                     "confirm_password": "usersecretpass"}

        # User sample details to login
        self.user_login = {"email": "peris@andela.com",
                           "password": "usersecretpass"}

        # User email to borrow and return book
        self.user_email = {"email": "peris@andela.com"}

        with self.app.app_context():
            db.create_all()

    def add_books_test_db(self):
        """Add two books in tests db."""
        access_token = TestAdminEndpoints.register_login_admin(self)

        # Add a new book with an admin access token
        self.client.post('/api/v2/books', data=json.dumps(self.book),
                         headers={'content-type': 'application/json',
                                  'Authorization': 'Bearer {}'
                                  .format(access_token)})
        # Add a second book
        self.client.post('/api/v2/books', data=json.dumps(self.book_two),
                         headers={'content-type': 'application/json',
                                  'Authorization': 'Bearer {}'
                                  .format(access_token)})

    def test_borrow_book(self):
        """Test if get all books endpoints works as expected route."""
        # Get user access_token
        access_token = TestAdminEndpoints.register_login_user(self)
        # Try to borrow a book without passwing your email
        response = self.client.post(
            '/api/v2/users/books/1', data=json.dumps({}),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'
                     .format(access_token)})
        self.assertIn("Enter your email to continue", str(response.data))

        # Try to borrow a book that does not exist
        response = self.client.post(
            '/api/v2/users/books/1', data=json.dumps(self.user_email),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'
                     .format(access_token)})
        self.assertIn("No book with that Id.", str(response.data))

        # Add books to borrow
        self.add_books_test_db()

        # Borrow the first book added above
        response = self.client.post(
            '/api/v2/users/books/1', data=json.dumps(self.user_email),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'
                     .format(access_token)})
        self.assertIn('Book borrowed successfully', str(response.data))
        self.assertIn('Data science for Dummies', str(response.data))

        # Try to borrow a book twice
        response = self.client.post(
            '/api/v2/users/books/1', data=json.dumps(self.user_email),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'
                     .format(access_token)})
        self.assertIn(
            'Somebody already borrowed this book', str(response.data))

    def test_return_book(self):
        """Test if get all books endpoints works as expected route."""
        # Get user access_token
        access_token = TestAdminEndpoints.register_login_user(self)
        # Add books to borrow and return
        self.add_books_test_db()

        # Borrow book two added above
        self.client.post(
            '/api/v2/users/books/2', data=json.dumps(self.user_email),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})

        # Try to ruturn a book is not borrowed
        response = self.client.put(
            '/api/v2/users/books/1', data=json.dumps(self.user_email),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'
                     .format(access_token)})
        self.assertIn("The book is not borrowed to return", str(response.data))

        # Ruturn book two borrowed above
        response = self.client.put(
            '/api/v2/users/books/2', data=json.dumps(self.user_email),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'
                     .format(access_token)})
        self.assertIn("Book returned successfully", str(response.data))
        self.assertIn("Winning start in your mind", str(response.data))

        # Try to ruturn a book with wrong book id
        response = self.client.put(
            '/api/v2/users/books/wxxw', data=json.dumps(self.user_email),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'
                     .format(access_token)})
        self.assertIn("Use a valid books Id", str(response.data))

    def test_get_user_borrow_history(self):
        """Test if get all books endpoints works as expected route."""
        # Get user access_token
        access_token = TestAdminEndpoints.register_login_user(self)
        # Add books to borrow
        self.add_books_test_db()

        # Try to get borrowing history of a user who has never borrowed
        response = self.client.get('/api/v2/users/books',
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'
                                            .format(access_token)})
        self.assertIn(
            "You do not have a borrowing history.", str(response.data))

        # Try to get books not returned
        response = self.client.get('/api/v2/users/books?returned=false',
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'
                                            .format(access_token)})
        self.assertIn(
            "You do not have a book that is not returned.", str(response.data))

        # Borrow the first book added above
        self.client.post('/api/v2/users/books/1',
                         data=json.dumps(self.user_email),
                         headers={'content-type': 'application/json',
                                  'Authorization': 'Bearer {}'
                                  .format(access_token)})

        # Borrow the second book added above
        self.client.post('/api/v2/users/books/2',
                         data=json.dumps(self.user_email),
                         headers={'content-type': 'application/json',
                                  'Authorization': 'Bearer {}'
                                  .format(access_token)})

        # Ruturn the second book borrowed above
        self.client.put(
            '/api/v2/users/books/2', data=json.dumps(self.user_email),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'
                     .format(access_token)})

        # Get the borrowing history of a user
        response = self.client.get('/api/v2/users/books',
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'
                                            .format(access_token)})
        self.assertIn("Data science for Dummies", str(response.data))
        self.assertIn("Winning start in your mind", str(response.data))

        # Get the books not returned a user
        response = self.client.get('/api/v2/users/books?returned=false',
                                   headers={'content-type': 'application/json',
                                            'Authorization': 'Bearer {}'
                                            .format(access_token)})
        self.assertIn("Data science for Dummies", str(response.data))
        self.assertNotIn("Winning start in your mind", str(response.data))

    def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
