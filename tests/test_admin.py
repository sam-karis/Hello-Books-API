"""Unittest for API book endpoints."""
import unittest
import json
# local imports.
from app import create_app, db
from app.models import User, Books


class TestAdminEndpoints(unittest.TestCase):
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

        # update of a book
        self.book_update = {"title": "The simple way into analytic"}

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
        self.user = {"name": "Jack",
                     "email": "jack@andela.com",
                     "password": "usersecretpass",
                     "confirm_password": "usersecretpass",}

        # User sample details to login
        self.user_login = {"email": "jack@andela.com",
                           "password": "usersecretpass"}

        with self.app.app_context():
            db.create_all()

    def register_login_admin(self):
        # Register a new admin
        self.client.post('/api/v2/auth/register', data=json.dumps(self.admin),
                         headers={'content-type': 'application/json'})

        # Login a admin
        login_response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin_login),
            headers={'content-type': 'application/json'})
        # Get admin access token
        access_token = json.loads(
            login_response.get_data().decode('utf-8'))['access_token']

        return access_token

    def register_login_user(self):
        # Register a new user
        self.client.post('/api/v2/auth/register', data=json.dumps(self.user),
                         headers={'content-type': 'application/json'})

        # Login a user
        login_response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_login),
            headers={'content-type': 'application/json'})
        # Get user access token
        access_token = json.loads(
            login_response.get_data().decode('utf-8'))['access_token']

        return access_token

    def test_admin_add_book(self):
        """Test if admin can add a book."""
        # Add a new book without an access token
        response = self.client.post(
            '/api/v2/books', data=json.dumps(self.book),
            headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing Authorization Header', str(response.data))

        # Get an admin access token
        access_token = self.register_login_admin()

        # Add a new book with an admin access token
        response = self.client.post(
            '/api/v2/books', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Book added successfully.', str(response.data))

        # Add a book that already exist
        response = self.client.post(
            '/api/v2/books', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        # Test that the endpoint does not allow addition a book twice
        self.assertIn('A book with that title already exist.',
                      str(response.data))

    def test_user_add_book(self):
        """Test if a non admin user can add a book."""
        # Get an user access token
        access_token = self.register_login_user()

        # Try to add a new book with an user access token
        response = self.client.post(
            '/api/v2/books', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Need to be an admin add a continue.',
                      str(response.data))

    def test_admin_delete_book(self):
        """Test admin can delete a book."""
        # Get an admin access token
        access_token = self.register_login_admin()

        # Delete a book that does not exist
        response = self.client.delete(
            '/api/v2/books/1', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertIn('No book with that Id.', str(response.data))

        # Add a new book
        self.client.post('/api/v2/books', data=json.dumps(self.book),
                         headers={'content-type': 'application/json',
                                  'Authorization': 'Bearer {}'
                                  .format(access_token)})

        # Try delete a book with an invalid id
        response = self.client.delete(
            '/api/v2/books/xcdcw', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertIn('Use a valid book Id', str(response.data))

        # Delete a book added above
        response = self.client.delete(
            '/api/v2/books/1', data=json.dumps(self.book),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertIn('Book deleted successfully', str(response.data))

    def test_modify_book(self):
        """Test if a modify book by admin endpoint works as expected."""
        # Get an admin access token
        access_token = self.register_login_admin()

        # Add a new book to modify
        self.client.post('/api/v2/books', data=json.dumps(self.book),
                         headers={'content-type': 'application/json',
                                  'Authorization': 'Bearer {}'
                                  .format(access_token)})

        # Modify a book added above
        response = self.client.put(
            '/api/v2/books/1', data=json.dumps(self.book_update),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertIn('Your update is successful.', str(response.data))

        # Logout the user to blacklist a token
        res = self.client.post(
            '/api/v2/auth/logout', data=json.dumps(self.admin_login),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})

        # Modify a book with a blacklisted token
        response = self.client.put(
            '/api/v2/books/1', data=json.dumps(self.book_update),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertIn('The token has been blacklisted.', str(response.data))

    def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
