"""Populate some data using python data stractures."""

from .models import Users, Admin, Books, BookHistory

# Populate some data for users
USERS = list()
user_1 = Users(1, 'Joan', 'joan@andela.com', 'secretpassword')
user_2 = Users(2, 'John', 'john@andela.com', 'hardpassword')
user_3 = Users(3, "Jane", 'jane@andela.com', 'cluelesspas')
USERS.append(user_1)
USERS.append(user_2)
USERS.append(user_3)

# Populate some data for admin
ADMIN = list()
admin_1 = Admin(1, 'Sam', 'sam@andela.com', 'hardtoguess')
admin_2 = Admin(2, 'peris', 'peris@andela.com', 'awesome4321')
ADMIN.append(admin_1)
ADMIN.append(admin_2)


# Populate some data for books
BOOKS = list()
book_1 = Books(
    1, 'Data Science', 'Rpeng', 'Intro to data science with python',
    '5th', '2001', 5
)
book_2 = Books(
    2, 'Data Science', 'Sam', 'Intermidiate to data science with python',
    '6th', '2017', 3
)
BOOKS.append(book_1)
BOOKS.append(book_2)
