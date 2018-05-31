# Hello-Books-API
[![Build Status](https://travis-ci.org/sam-karis/Hello-Books-API.svg?branch=master)](https://travis-ci.org/sam-karis/Hello-Books-API)  [![Maintainability](https://api.codeclimate.com/v1/badges/6a4b6e3805c74b78d14f/maintainability)](https://codeclimate.com/github/sam-karis/Hello-Books-API/maintainability) [![Coverage Status](https://coveralls.io/repos/github/sam-karis/Hello-Books-API/badge.svg?branch=Challenge-Three)](https://coveralls.io/github/sam-karis/Hello-Books-API?branch=Challenge-Three)

Hello-Books-APi is a library management API. It help in management and tracking of books and users who interact with the library's books. The API also enable new users to register while existing users can login. Users can also reset their password and borrow books.
The API functionality and the respective endpoints include the following:  

- To view documentation click [here](https://hellobookapi.docs.apiary.io/).   

|Endpoints and methods               | Functionality              |Authorized|
|------------------------------------|----------------------------|---------------------
|/api/v1/books (POST)                |Add a book                  | Admin only               
|/api/v1/books/*bookId*(PUT)         |Modify a book’s information | Admin only
|/api/v1/books/*bookId*(DELETE)      |Remove a book               | Admin only
|/api/v1/books(GET)                  |Retrieves all books         | Everybody
|/api/v1/books/*book_id*(GET)        |Get a book                  | Everybody
|/api/v1/users/books/*book_id*(POSt) |Borrow a book               | logged in User and Admin
|/api/v1/auth/register(POST)         |Register a user             | Everybody
|/api/v1/auth/register(PUT)          |Upgrade a user to admin     | Admin only
|/api/v1/auth/register(GET)          |Get registered users        | Admin only
|/api/v1/auth/login(POST)            |Login a user                | Registered user
|/api/v1/auth/logout(POST)           |Logout a user               | Loggged in user
|/api/v1/auth/reset-password(POST)   |Reset a user Password       | Registered user
|/api/v1/users/books/*book_id*(POST) |Borrow a books              |Logged in user
|/api/v1/users/books/*book_id*(PUT)  |Return a books              |Logged in user
|/api/v1/users/books(GET)            |Get user borrowing history  |Logged in user

#### Running and Testing of the API

**Prequisites**
```
Python - version 3.6.4
Postgress database
postman - To run various endponts
```
**Installing**   

Perform the following simple steps:   
- Open git and navigate to directory yo which to run the app from.
- Git clone the this repository using either.
  - Using SSH:
    
    ``git@github.com:sam-karis/Hello-Books-API.git``
  
  - Using HTTP:
    
    ``https://github.com/sam-karis/Hello-Books-API.git``

- Set up a virtual eniviroment for reference click [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

- Activate the virtualenv on your terminal

- Now install the apps dependencies by running `pip install -r requirements.txt`

- Create databaseand set global variables on the terminal  
  - For database set `DATABASE_URL= 'yourdatabaseurl'`
  - For email sending   
  `Email='defaultmail@example.com'`   
  `Username='yourusername'`   
  `Password='dmy_password'`

- Run manage.py to create database tables as below   
    `python manage.py db init`   
    `python manage.py db migrate`   
    `python manage.py db upgrade`


- Set the following configuration on terminal to run the app``FLASK_CONFIG=development, FLASK_APP=run.py``
- Then run ``flask run`` to launch the localhost.
- Lastly with the app running access the endpoints using postman.

While working with postman use the following attributes:
- For adding and editing books - ``title``, ``description``, ``edition``, ``author``
- User registration - ``name``, ``email`` ,``password``
- User login - ``email ``,  ``password``
- User logout, borrow  and returnbook,  - ``email``
- User reset password - ``email``,  ``new_password``

**Tests**
Hello-Books-API has automated test(unittest) to check if it the endpoints work as expected. To run the tests activate the virtual environment and then run `nosetests --with-coverage`

**To contribute to this work**

Fork the repository from links shared above and make a pull request.