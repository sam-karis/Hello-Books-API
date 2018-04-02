"""Populate some data using python data stractures."""

from .models import Users, Admin, Books, BookHistory

# Populate some data for users
USERS = list()
user_1 = Users(1, 'Joan', 'joan@andela.com', 'secretpassword')
user_1.hash_password('secretpassword')
user_2 = Users(2, 'John', 'john@andela.com', 'hardpassword')
user_2.hash_password('hardpassword')
user_3 = Users(3, "Jane", 'jane@andela.com', 'cluelesspass')
user_3.hash_password('cluelesspass')
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
    1, 'Data Science', 'Rpeng', 'Intro to data science with python', '5th'
)
book_2 = Books(
    2, 'Data Mining', 'Sam', 'Intermidiate to data science with SQL', '6th'
)
BOOKS.append(book_1)
BOOKS.append(book_2)

BOOKHISTORY = list()
