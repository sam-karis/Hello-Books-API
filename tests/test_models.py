"""Unit test for different models."""
import unittest

# local imports
from app.models import users, admin, books, bookHistory


class TestModels(unittest.TestCase):
    """Test if all models are working."""

    def test_user_model(self):
        """Test number of users."""
        Users = list()
        Users.append(users(1, 'Joan', 'joan@andela.com', 'secretpassword'))
        self.assertEqual(len(Users), 1)

    def test_admin_model(self):
        """Test number of admin."""
        Admin = list()
        Admin.append(admin(1, 'Sam', 'sam@andela.com', 'hardtoguess'))
        Admin.append(admin(2, 'Rose', 'rose@andela.com', 'privatepassword'))
        self.assertEqual(len(Admin), 2)

    def test_books_model(self):
        """Test number of books."""
        Books = list()
        Books.append(books(1, 'Data Science', 'Rpeng', '5th',
                           'Intro to data science with python', '2001', 5))
        self.assertEqual(len(Books), 1)

    def test_bookHistory_model(self):
        """Test number of bookHistory ever borrowed."""
        BookHistory = list()
        BookHistory.append(bookHistory('Data Science', '1',
                                       '12-3-2013', '12-4-2013', 'Returned'))
        self.assertEqual(len(BookHistory), 1)


if __name__ == '__main__':
    unittest.main()
