from pytest import fixture
from app.models import User, Todo
from app import create_app, db
from base64 import b64encode


def generate_todos(user_id):
    for item in range(3):
        todo = Todo(
            text=f'something{item}',
            complete=False,
            user_id=user_id
        )

        db.session.add(todo)
        db.session.commit()

def generate_data():
    u1 = User(
        username='test',
        password='pass12A@',
        admin_role=False
    )

    u2 = User(
        username='admin',
        password='pass12A@',
        admin_role=True
    )

    u3 = User(
        username='edit',
        password='pass12A@',
        admin_role=False
    )

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)

    db.session.commit()

    generate_todos(u1.id)
    generate_todos(u2.id)
    generate_todos(u2.id)
    


@fixture
def application():
    # set up
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    generate_data()

    yield app
    
    # teardown
    db.session.remove()
    db.drop_all()
    app_context.pop()



def get_jwt(test_client, username):
    user = User.query.filter_by(username=username).first()
    
    credentials = b64encode(f"{user.username}:pass12A@".encode('utf-8')).decode('utf-8')

    response = test_client.get(
        '/api/v1/login',
        headers={"Authorization": f"Basic {credentials}"}
    )

    assert response.status_code == 200
    assert response.get_json().get('token', False)
    token = response.get_json()['token']
    
    return token

