from base64 import b64encode
from .helper import application


def test_login(application):
    test_client = application.test_client()

    credentials = b64encode(b"test:pass12A@").decode('utf-8')

    response = test_client.get(
        '/api/v1/login',
        headers={"Authorization": f"Basic {credentials}"}
    )

    assert response.status_code == 200
    
    token = response.get_json().get('token', '')
    assert token != ''


def test_login_unauthorized(application):
    test_client = application.test_client()

    credentials = b64encode(b"test:pass12A@").decode('utf-8')

    response = test_client.get(
        '/api/v1/login'
    )

    assert response.status_code == 401
    
    msg = response.get_json().get('msg', False)
    assert msg == 'Could not verify user'


def test_login_user_notfound(application):
    test_client = application.test_client()

    credentials = b64encode(b"ttt:pass12A@").decode('utf-8')

    response = test_client.get(
        '/api/v1/login',
        headers={"Authorization": f"Basic {credentials}"}
    )

    assert response.status_code == 404
    assert response.get_json() == {'error': 'Not found'}
