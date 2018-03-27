"""Unit test for different models."""
import unittest

# local imports
from app.models import Users, Admin, Books, BookHistory


class TestModels(unittest.TestCase):
    """Test if all models are working."""

    def test_user_model(self):
        """Test number of users."""
        USER = list()
        USER.append(Users(1, 'Joan', 'joan@andela.com', 'secretpassword'))
        self.assertEqual(len(USER), 1)

    def test_admin_model(self):
        """Test number of admin."""
        ADMIN = list()
        ADMIN.append(Admin(1, 'Sam', 'sam@andela.com', 'hardtoguess'))
        ADMIN.append(Admin(2, 'Joan', 'joan@andela.com', 'hardtoguess'))
        self.assertEqual(len(ADMIN), 2)
        self.assertEqual(ADMIN[0].name, 'Sam')

    def test_books_model(self):
        """Test number of books."""
        BOOK = list()
        BOOK.append(Books(1, 'Data Science', 'Rpeng', '5th',
                           'Intro to data science with python', '2001', 5))
        self.assertEqual(len(BOOK), 1)
        self.assertEqual(BOOK[0].title, 'Data Science')

    def test_bookHistory_model(self):
        """Test number of bookHistory ever borrowed."""
        BOOKHISTORY = list()
        BOOKHISTORY.append(BookHistory('Data Science', '1',
                                       '12-3-2013', '12-4-2013', 'Returned'))
        self.assertEqual(len(BOOKHISTORY), 1)


if __name__ == '__main__':
    unittest.main()
