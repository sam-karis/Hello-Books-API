# Hello-Books-API
[![Build Status](https://travis-ci.org/sam-karis/Hello-Books-API.svg?branch=master)](https://travis-ci.org/sam-karis/Hello-Books-API)  [![Maintainability](https://api.codeclimate.com/v1/badges/6a4b6e3805c74b78d14f/maintainability)](https://codeclimate.com/github/sam-karis/Hello-Books-API/maintainability) [![Coverage Status](https://coveralls.io/repos/github/sam-karis/Hello-Books-API/badge.svg?branch=Challenge-Three)](https://coveralls.io/github/sam-karis/Hello-Books-API?branch=Challenge-Three)

Hello-Books-APi is a library management API. It help in management and tracking of books and users who interact with the library's books. The API also enable new users to register while existing users can login. Users can also reset their password and borrow books.
The API functionality and the respective endpoints include the following:

|Endpoint                        | Functionality              | 
|--------------------------------|----------------------------
|/api/v1/books                   |Add a book                   |  
|/api/v1/books/*bookId*          |Modify a book’s information |
|/api/v1/books/*bookId*          |Remove a book                |
|/api/v1/books                   |Retrieves all books          |
|/api/v1/books/*book_id*         |Get a book                  |
|/api/v1/users/books/*book_id*   |Borrow a book               |
|/api/v1/auth/register           |Register a user             |
|/api/v1/auth/login              |Login a user               |
|/api/v1/auth/logout             |Logout a user              |
|/api/v1/auth/reset-password     |Reset a user Password      |

#### Running and Testing of the API

**Prequisites**
```
Python - version 3.6.4
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

- Set the following ``FLASK_CONFIG=development, FLASK_APP=run.py``
- Then run ``flask run`` to launch the localhost.
- Lastly with the app running access the endpoints using postman.

While working with postman use the following attributes:
- For adding and editing books
``book_id`` ``title`` ``description`` ``edition`` ``quantity`` ``pyear``
- User registration
``name`` ``user_id`` ``email`` ``password``
- User login
``email``  ``password``

**Tests**
Hello-Books-API has automated test(unittest) to check if it the endpoints work as expected. To run the navigate to test folder and you can run the through the terminal.

**To contribute to this work**

Fork the repository from links shared above and make a pull request.