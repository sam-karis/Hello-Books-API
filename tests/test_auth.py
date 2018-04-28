"""Unittest for API endpoints."""
import unittest
import json
# local imports.
from app import create_app, db
from app.models import User


class TestAuthEndpoints(unittest.TestCase):
    """Test books endpoints."""

    def setUp(self):
        """SetUp test."""
        config_name = 'testing'
        self.app = create_app(config_name)
        self.client = self.app.test_client()

        # User sample details to test register
        self.user = {"name": "Jack",
                     "email": "jack@andela.com",
                     "password": "usersecretpass"}

        # User sample details to test login
        self.user_login = {"email": "jack@andela.com",
                           "password": "usersecretpass"}

        # User sample details to test password reset
        self.user_reset = {"email": "jack@andela.com",
                           "password": "userresetpass"}

        # User sample details to test logout
        self.user_logout = {"email": "jack@andela.com"}

        # Wrong User sample details to test login
        self.user_wrong_login = {"email": "jack@andela.com",
                                 "password": "wrongsecretpass"}

        # Admin sample details to test register
        self.admin = {"name": "samkaris",
                      "email": "samkaris@andela.com",
                      "password": "adminsecretpass",
                      "is_admin": True}

        with self.app.app_context():
            db.create_all()

    def test_register_user(self):
        """Test if  registering a user work as expected."""
        # Register a new user
        response = self.client.post(
            '/api/v2/auth/register', data=json.dumps(self.user),
            headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully registered as a User', str(response.data),
                      msg="Register new user successfully")
        # Register a user twice
        response_two = self.client.post(
            '/api/v2/auth/register', data=json.dumps(self.user),
            headers={'content-type': 'application/json'})
        self.assertIn('Email already registered to another user',
                      str(response_two.data),
                      msg="Cant register same user twice")

    def test_register_admin(self):
        """Test if  registering an admin work as expected."""
        # Register a new admin
        response = self.client.post(
            '/api/v2/auth/register', data=json.dumps(self.admin),
            headers={'content-type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully registered as an Admin',
                      str(response.data),
                      msg="Register new Admin successfully")

        # Register an admin twice
        response_two = self.client.post(
            '/api/v2/auth/register', data=json.dumps(self.admin),
            headers={'content-type': 'application/json'})
        self.assertIn('Email already registered to another user',
                      str(response_two.data),
                      msg="Cant register same admin twice twice")

    def test_login_user(self):
        """Test if  login endpoint work as expected."""
        # Register a user to login
        self.client.post('/api/v2/auth/register', data=json.dumps(self.user),
                         headers={'content-type': 'application/json'})

        # Login a user
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_login),
            headers={'content-type': 'application/json'})
        # Test if login was successful with right credentials
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfuly login', str(response.data),
                      msg="Login successful")
        self.assertIn('access_token', str(response.data),
                      msg="Access token issued")

        # Login a user already logged in
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_login),
            headers={'content-type': 'application/json'})
        # Test if login was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn('You are already logged In', str(response.data),
                      msg="Login successful")

        # Login a user without password
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(
                {"email": "jack@andela.com"}),
            headers={'content-type': 'application/json'})
        # Test if login was successful with right credentials
        self.assertIn('Enter a valid password', str(response.data),
                      msg="Login successful")

        # Login a user with wrong credentials
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_wrong_login),
            headers={'content-type': 'application/json'})
        # Test if login was successful with wrong credentials
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid email or password',
                      str(response.data), msg="Login successful")
        self.assertNotIn('access_token', str(response.data),
                         msg="Access token not issued")

    def test_logout_user(self):
        """Test if  logout endpoint work as expected."""
        # Register a user
        self.client.post('/api/v2/auth/register', data=json.dumps(self.user),
                         headers={'content-type': 'application/json'})
        # Login a user
        login_response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user_login),
            headers={'content-type': 'application/json'})
        # Get access token
        access_token = json.loads(
            login_response.get_data().decode('utf-8'))['access_token']

        # Logout a user
        response = self.client.post(
            '/api/v2/auth/logout', data=json.dumps(self.user_logout),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Successfuly logged Out', response.get_data().decode('utf-8'),
            msg="Logout successful")

        # Logout a user who is logged out
        response = self.client.post(
            '/api/v2/auth/logout', data=json.dumps(self.user_logout),
            headers={'content-type': 'application/json',
                     'Authorization': 'Bearer {}'.format(access_token)})
        email = self.user_logout['email']
        self.assertIn(
            '{} is not logged In or token has been blacklisted'.format(email),
            response.get_data().decode('utf-8'),
            msg="Logout successful")

    def test_password_reset(self):
        """Test for  password-reset endpoint."""
        # Reset password of a user not registered
        response = self.client.post(
            '/api/v2/auth/reset-password',
            data=json.dumps(self.user_login),
            headers={'content-type': 'application/json'})
        email = self.user_login['email']
        self.assertIn('No user registered with {} as their email'
                      .format(email), str(response.data))

        # Register a user to reset-password
        self.client.post('/api/v2/auth/register', data=json.dumps(self.user),
                         headers={'content-type': 'application/json'})

        # Try to reset to the same password
        response = self.client.post(
            '/api/v2/auth/reset-password',
            data=json.dumps(self.user_login),
            headers={'content-type': 'application/json'})
        self.assertIn('Current password used thus no reset.',
                      str(response.data))

        # Reset password
        response = self.client.post(
            '/api/v2/auth/reset-password',
            data=json.dumps(self.user_reset),
            headers={'content-type': 'application/json'})
        self.assertIn('Reset successful.', str(response.data))

    def tearDown(self):
        """Return to normal state after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
