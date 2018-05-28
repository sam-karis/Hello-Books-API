import os
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

# Local imports
from app import create_app, mail

app = create_app(os.getenv('FLASK_CONFIG'))


def generate_reset_password_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_reset_password_token(token, exipiration=600):
    serializer = URLSafeTimedSerializer(app.config['SECRET'])
    try:
        email = serializer.loads(
            token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=exipiration)
    except:
        return False
    return email


def send_email(To, Subject):
    msg = Message(subject='Password Reset Token', recipients=[To],
                  html='<p> To reset your password use this token :'
                  ' <a href="#"><strong>{}</strong></a></p>'.format(Subject))
    mail.send(msg)
