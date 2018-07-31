import os
import click
from flask import Flask
from flask.cli import with_appcontext
from app import create_app
from app.models import User
from app.auth.views import validate_email

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


@click.command()
@click.option('--name', prompt='Enter Admin full name', help='Admin Full names.')
@click.option('--username', prompt='Enter Admin username', help='Admin username.')
@click.option('--email', prompt='Enter Admin email', help='Admin email.')
@click.password_option('--password', prompt='Enter Admin password', help='Admin password more than 6 characters.')
@with_appcontext
def create_admin(name, username, email, password):
    person = User.get_user_by_email(email)
    if person:
        click.echo("User with that email exist")
        exit()
    if not validate_email(email) or len(password) < 6:
        click.echo("Invalid email and password.")
        exit()

    new_admin = User(name=name, email=email.strip(), username=username)
    new_admin.is_admin = True
    new_admin.hash_password(password)
    new_admin.save()

    click.echo("Admin added successfully")


if __name__ == '__main__':
    create_admin()
