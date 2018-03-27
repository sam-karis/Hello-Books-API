"""Populate some data using python data stractures."""

from .models import users, admin, books, bookHistory

# Populate some data for users
USERS = list()
user1 = users(1, 'Joan', 'joan@andela.com', 'secretpassword')
user2 = users(2, 'John', 'john@andela.com', 'hardpassword')
user3 = users(3, "Jane", 'jane@andela.com', 'cluelesspas')
USERS.append(user1)
USERS.append(user2)
USERS.append(user3)

# Populate some data for admin
ADMIN = list()
admin1 = admin(1, 'Sam', 'sam@andela.com', 'hardtoguess')
admin2 = admin(2, 'peris', 'peris@andela.com', 'awesome4321')
ADMIN.append(admin1)
ADMIN.append(admin2)


# Populate some data for books
BOOKS = list()
book1 = books(1, 'Data Science', 'Rpeng', 'Intro to data science with python',
              '5th', '2001', 5)
book2 = books(2, 'Data Science', 'Sam', 'Intermidiate to data science with python',
              '6th', '2017', 3)
BOOKS.append(book1)
BOOKS.append(book2)
