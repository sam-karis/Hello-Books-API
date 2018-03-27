"""Unittest for API endpoints."""
import unittest
import json
from flask import jsonify

# local imports.
from app import app, create_app
from app.models import Books


class TestBase(unittest.TestCase):
    """Test api endpoints."""

    def setUp(self):
        """SetUp test."""
        config_name = 'testing'
        app = create_app(config_name)
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        book_1 = Books(3, 'Data Sience', 'Rpeng', '5th',
                       'Intro to data science with python', '2001', 5)

        self.book = book_1.serialize

    def test_index(self):
        """Test index route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_book(self):
        """Test add a book endpoint."""
        response = self.client.post('/api/v1/books',
                                    data=json.dumps(self.book))
        self.assertEqual(response.status_code, 200)

    def test_get_all_books(self):
        """Test get book route."""
        response = self.client.get('/api/v1/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Data Science', str(response.data))

    def test_get_book(self):
        """Test get book route."""
        response = self.client.get('/api/v1/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Data Science', str(response.data))

    def tearDown(self):
        """End test."""
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()
