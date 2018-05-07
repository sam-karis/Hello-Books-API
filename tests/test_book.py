"""Unittest for API book endpoints."""
import unittest
import json
# local imports.
from app import create_app, db
from app.models import Books
from tests.test_admin import TestAdminEndpoints


class TestBookEndpoints(unittest.TestCase):
    """Test books endpoints."""

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
                      "is_admin": True}

        # Admin sample details to login
        self.admin_login = {"email": "samkaris@andela.com",
                            "password": "adminsecretpass"}

        with self.app.app_context():
            db.create_all()

    def test_get_all_books(self):
        """Test if get all books endpoints works as expected route."""
        # Get books when the library is empty
        response = self.client.get('/api/v2/books')
        self.assertEqual(response.status_code, 204,
                         msg="No books in the library")

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

        # Test the book added is in all books
        response = self.client.get('/api/v2/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Data science for Dummies', str(response.data),
                      msg="First book is retrieved successfully")
        self.assertIn('Winning start in your mind', str(response.data),
                      msg="Second book is retrieved successfully")

    def test_get_one_book_by_id(self):
        """Test if get all books endpoints works as expected route."""
        # Get book that does not exist
        response = self.client.get('/api/v2/books/1')
        self.assertIn("No book with that Id.", str(response.data),
                      msg="No books in the library")

        # Get book with invalid Id
        response = self.client.get('/api/v2/books/xxwws')
        self.assertIn("Use a valid book Id", str(response.data),
                      msg="No books in the library")

        # Get admin access_token
        access_token = TestAdminEndpoints.register_login_admin(self)

        # Add a new book with an admin access token
        self.client.post('/api/v2/books', data=json.dumps(self.book),
                         headers={'content-type': 'application/json',
                                  'Authorization': 'Bearer {}'
                                  .format(access_token)})

        # Test the book added is in all books
        response = self.client.get('/api/v2/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Data science for Dummies', str(response.data),
                      msg="First book is retrieved successfully")

    def test_wrong_endpoint_url(self):
        """Test if api handles wrong url."""
        # Try to get a book from wrong url
        response = self.client.get('/api/v2/booooks')
        self.assertIn("http://localhost/api/v2/booooks is not a valid url",
                      str(response.data), msg="Handles invalid url")

    def test_wrong_request_method(self):
        """Test if api handles wrong url."""
        # Try to use a wrong request method on valid endpoint
        response = self.client.delete('/api/v2/books')
        self.assertIn("The DELETE method is not allowed for this endpoint",
                      str(response.data), msg="Handles wrong request method")

    def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
