import os
"""Random string used to generate hashes that secure things in an app."""
SECRET = "qwerty098765mnbvcxzmnbvcxz"
SESSION_TYPE = "qwerty098765mnbvcxzmnbvcxz"
SECURITY_PASSWORD_SALT = 'poiuytrewq987654321'

# Mail configurations
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('Username')
MAIL_DEFAULT_SENDER = os.environ.get('Email')
MAIL_PASSWORD = os.environ.get('Password')
