from .helper import get_jwt, application


def test_get_all_users(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.get(
        '/api/v1/user',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.get_json().get('users', False)


def test_get_all_users_without_jwt(application):
    test_client = application.test_client()

    response = test_client.get(
        '/api/v1/user'
    )

    assert response.status_code == 401

    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'


def test_get_user(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.get(
        '/api/v1/user/1',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200

    data = response.get_json().get('user', False)
    assert isinstance(data, dict)


def test_get_user_without_jwt(application):
    test_client = application.test_client()

    response = test_client.get(
        '/api/v1/user/1'
    )

    assert response.status_code == 401

    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'


def test_get_user_not_found_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.get(
        '/api/v1/user/100',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    assert response.get_json() == {'error': 'Not found'}


def test_create_user(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'admin')
    response = test_client.post(
        '/api/v1/user',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'test2', 'password': 'test2'}
    )

    assert response.status_code == 201
    
    msg = response.get_json().get('msg', False)
    assert msg == 'user test2 has been created successfuly'


def test_create_user_permission_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.post(
        '/api/v1/user',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'test2', 'password': 'test2'}
    )

    assert response.status_code == 403

    msg = response.get_json().get('msg', False)
    assert msg == 'admin permission required'


def test_create_user_mimetype_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.post(
        '/api/v1/user',
        headers={'Authorization': f'Bearer {token}'},
        data={'username': 'test2', 'password': 'test2'}
    )

    assert response.status_code == 400
    
    msg = response.get_json().get('msg', False)
    assert msg == 'mimetype is not valid'


def test_create_user_not_valid_data(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'admin')
    response = test_client.post(
        '/api/v1/user',
        headers={'Authorization': f'Bearer {token}'},
        json={'username2': 'test2', 'password': 'test2'}
    )

    assert response.status_code == 400
    
    msg = response.get_json().get('msg', False)
    assert msg == 'user data is not valid'


def test_edit_user(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'admin')
    response = test_client.put(
        '/api/v1/user/3',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'edit2', 'password': 'test2'}
    )

    assert response.status_code == 200

    msg = response.get_json().get('msg', False)
    assert msg == 'user data has been changed'


def test_edit_user_notfound_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'admin')
    response = test_client.put(
        '/api/v1/user/300',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'edit2', 'password': 'test2'}
    )

    assert response.status_code == 404
    
    msg = response.get_json().get('msg', False)
    assert msg == 'user not found'


def test_edit_user_permission_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.put(
        '/api/v1/user/3',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'edit2', 'password': 'test2'}
    )

    assert response.status_code == 403

    msg = response.get_json().get('msg', False)
    assert msg == 'admin permission required'


def test_edit_user_without_jwt(application):
    test_client = application.test_client()

    response = test_client.put(
        '/api/v1/user/3',
        json={'username': 'edit2', 'password': 'test2'}
    )

    assert response.status_code == 401

    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'



def test_delete_user(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'admin')
    response = test_client.delete(
        '/api/v1/user/3',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    
    msg = response.get_json().get('msg', False)
    assert msg == 'user has been deleted'


def test_delete_user_notfound_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'admin')
    response = test_client.delete(
        '/api/v1/user/300',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    
    msg = response.get_json().get('msg', False)
    assert msg == 'user not found'


def test_delete_user_permission_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.delete(
        '/api/v1/user/3',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 403
    
    msg = response.get_json().get('msg', False)
    assert msg == 'admin permission required'


def test_delete_user_witout_jwt(application):
    test_client = application.test_client()

    response = test_client.delete(
        '/api/v1/user/3'
    )

    assert response.status_code == 401
    
    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'

