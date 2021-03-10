from os import getenv
from app import create_app, db


app = create_app(getenv('FLASK_CONFIG') or 'default')

