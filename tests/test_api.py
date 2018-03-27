"""Unittest for API endpoints."""
import unittest
import json

# local imports.
from app import app, create_app
from app.models import books


class TestBase(unittest.TestCase):
    """Test api endpoints."""

    def setUp(self):
        config_name = 'testing'
        app = create_app(config_name)
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        book1 = books(1, 'Data Science', 'Rpeng', '5th',
                      'Intro to data science with python', '2001', 5)

        self.book = book1.serialize

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        """Test index route."""
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'WELCOME TO HELLO BOOKS!')

    def test_add_book_handler(self):
        """Test add a book endpoint."""
        response = self.client.post('/api/v1/books',
                                    data=json.dumps(self.book))
        self.assertEqual(response.status_code, 200)

    def test_get_book_handler(self):
        """Test get book route."""
        response = self.client.get('/api/v1/books', )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
