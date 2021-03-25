from os import getenv
from app import create_app, db
from app.models import User, Todo


app = create_app(getenv('FLASK_CONFIG', 'default'))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Todo=Todo)
