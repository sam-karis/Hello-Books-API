"""Unittest for API endpoints."""
import unittest
import json
from flask import jsonify

# local imports.
from app import app, create_app
from app.models import Books, Users
# from app.setup_data import BOOKS, USERS


class TestBooksEndpoints(unittest.TestCase):
    """Test books endpoints."""

    def setUp(self):
        """SetUp test."""
        config_name = 'testing'
        app = create_app(config_name)
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        book_one = Books(3, 'Data Sience for Dummies', 'Rpeng', '5th',
                         'Intro to data science with python', '2001', 5)

        self.book_one_update = {
            "author": "Justmesam",
            "title": "My journey to Andela"
        }

        self.book = book_one.serialize

        # User sample details to register
        user_one = Users(10, "Jack", 'jack@andela.com', "secretpass")
        self.user = user_one.serialize

        # User details to login
        self.user_login_details = {
            "email": "jack@andela.com",
            "password": "secretpass"
        }

        self.user_one_reset = {
            "email": "jack@andela.com",
            "password": "uniquepass"
        }

    def tearDown(self):
        """Return to normal state after test."""
        self.app_context.pop()

    def test_add_book(self):
        """Test add a book endpoint."""
        # Add a new book
        response = self.client.post('/api/v1/books',
                                    data=json.dumps(self.book),
                                    headers={
                                        'content-type': 'application/json'
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book added successfully.',
                      response.get_data().decode('utf-8'),
                      msg="Book added successfully")

        # Add a book that already exist
        response_two = self.client.post('/api/v1/books',
                                        data=json.dumps(self.book),
                                        headers={
                                            'content-type': 'application/json'
                                        })
        # Test that the endpoint does not add two similar books
        self.assertIn('A book with that title already exist.',
                      response_two.get_data().decode('utf-8'),
                      msg="Book cannot be added twice")

        # delete the book after test
        self.client.delete('/api/v1/books/3')

    def test_get_all_books(self):
        """Test get all book route."""
        # Add a book
        response = self.client.post('/api/v1/books',
                                    data=json.dumps(self.book),
                                    headers={
                                        'content-type': 'application/json'
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book added successfully.', str(response.data),
                      msg="Book added successfully")

        # Test the book added is in all books
        response = self.client.get('/api/v1/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Data Sience for Dummies', str(response.data),
                      msg="Books added retrieved successfully")

        # delete the book after test
        self.client.delete('/api/v1/books/3')

    def test_get_book(self):
        """Test get book route."""
        # Try and get a book with an Id that does not exist
        response = self.client.get('/api/v1/books/3')
        self.assertIn('No book with that Id.', str(response.data),
                      msg="Cannot get a book that does not exist.")

        # Add a book to get
        self.client.post('/api/v1/books',
                         data=json.dumps(self.book),
                         headers={'content-type': 'application/json'})

        # Get the book added
        response = self.client.get('/api/v1/books/3')
        self.assertIn('Data Sience for Dummies', str(response.data),
                      msg="Getting a book by Id successful")

        # delete the added book after test
        self.client.delete('/api/v1/books/3')

    def test_delete_book(self):
        """Test delete book route."""
        # Add a book to delete
        self.client.post('/api/v1/books',
                         data=json.dumps(self.book),
                         headers={'content-type': 'application/json'})

        # Delete and confirm the book does not exist
        response = self.client.delete('/api/v1/books/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Book deleted successfully", str(response.data),
                      msg="Book deleted successfully")

        # Delete a book twice
        response = self.client.delete('/api/v1/books/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn("No book with that Id to delete.", str(response.data))

    def test_modify_book(self):
        """Test update book endpoint."""
        # Add the book to be updated

        self.client.post('/api/v1/books',
                         data=json.dumps(self.book),
                         headers={'content-type': 'application/json'})

        # Update the books title and author
        response = self.client.put('/api/v1/books/3',
                                   data=json.dumps(self.book_one_update),
                                   headers={
                                       'content-type': 'application/json'
                                   })
        self.assertIn('Your update is successful.', str(response.data),
                      msg="Book updated successfully")

        # delete the added book after test
        self.client.delete('/api/v1/books/3')

    """Test auth endpoints."""

    def test_register_user(self):
        """Test if  register endpoint work as expected."""
        # Register a new user
        response = self.client.post('/api/v1/auth/register',
                                    data=json.dumps(self.user),
                                    headers={
                                        'content-type': 'application/json'
                                    })
        self.assertEqual(response.status_code, 200,
                         msg="Register new user successfully")

        # Register a user twice
        response_two = self.client.post('/api/v1/auth/register',
                                        data=json.dumps(self.user),
                                        headers={
                                            'content-type': 'application/json'
                                        })
        self.assertIn('User already registered', str(response_two.data),
                      msg="Cant register one user twice")

    def test_login_user(self):
        """Test if  login endpoint work as expected."""
        # Add user to login
        self.client.post('/api/v1/auth/register',
                         data=json.dumps(self.user),
                         headers={
                             'content-type': 'application/json'
                         })
        # Login a user
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.user_login_details),
                                    headers={
                                        'content-type': 'application/json'
                                    })
        # Test if login was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfuly login',
                      response.get_data().decode('utf-8'),
                      msg="Login successful")

    def test_logout_user(self):
        """Test if  login endpoint work as expected."""
        self.client.post('/api/v1/auth/login',
                         data=json.dumps(self.user_login_details),
                         headers={
                             'content-type': 'application/json'
                         })
        # Logout a user
        response = self.client.post('/api/v1/auth/logout',
                                    data=json.dumps(self.user_login_details),
                                    headers={
                                        'content-type': 'application/json'
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfuly logged Out',
                      response.get_data().decode('utf-8'),
                      msg="Logout successful")

    def test_password_reset(self):
        """Test for  password-reset endpoint."""
        # Reset password
        response = self.client.post('/api/v1/auth/reset-password',
                                    data=json.dumps(self.user_one_reset),
                                    headers={
                                        'content-type': 'application/json'
                                    })
        self.assertIn('Reset successful', str(response.data),
                      msg="Reset successful")

        # Login with new password
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.user_one_reset),
                                    headers={
                                        'content-type': 'application/json'
                                    })
        self.assertIn('Successfuly login', str(response.data),
                      msg="Login with new password successful")


if __name__ == '__main__':
    unittest.main()
