from .helper import get_jwt, application


def test_get_all_todos(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.get(
        '/api/v1/todo',
        headers={'Authorization': f'Bearer {token}'}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data.get('todos', False), list)


def test_get_all_todos_without_jwt(application):
    test_client = application.test_client()

    response = test_client.get(
        '/api/v1/todo'
    )

    assert response.status_code == 401

    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'
   

def test_create_todo(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.post(
        '/api/v1/todo',
        headers={'Authorization': f'Bearer {token}'},
        json={'text': '123'}
    )

    assert response.status_code == 201

    msg = response.get_json().get('msg', False)
    assert msg == 'todo has been created successfuly'


def test_create_todo_validationerror(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.post(
        '/api/v1/todo',
        headers={'Authorization': f'Bearer {token}'},
        json={'text1': '123'}
    )

    assert response.status_code == 400

    msg = response.get_json().get('msg', False)
    assert msg == 'todo data is not valid'


def test_create_todo_without_jwt(application):
    test_client = application.test_client()

    response = test_client.post(
        '/api/v1/todo',
        json={'text': '123'}
    )

    assert response.status_code == 401

    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'


def test_create_todo_mimetype_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.post(
        '/api/v1/todo',
        headers={'Authorization': f'Bearer {token}'},
        data={'text': '123'}
    )

    assert response.status_code == 400

    msg = response.get_json().get('msg', False)
    assert msg == 'mimetype is not valid'


def test_get_todo(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.get(
        '/api/v1/todo/1',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200

    data = response.get_json().get('todo', False)
    assert isinstance(data, dict)


def test_get_todo_notfound(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.get(
        '/api/v1/todo/100',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    msg = response.get_json().get('msg', False)
    assert msg == 'todo 100 not found'


def test_get_todo_without_jwt(application):
    test_client = application.test_client()

    response = test_client.get(
        '/api/v1/todo/1'
    )

    assert response.status_code == 401
    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'


def test_edit_todo(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.put(
        '/api/v1/todo/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'text': '123'}
    )

    assert response.status_code == 200

    msg = response.get_json().get('msg', False)
    assert msg == 'todo data has been changed'


def test_edit_todo_without_jwt(application):
    test_client = application.test_client()

    response = test_client.put(
        '/api/v1/todo/1',
        json={'text': '123'}
    )

    assert response.status_code == 401

    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'


def test_edit_todo_validationerror(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.put(
        '/api/v1/todo/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'text1': '123'}
    )

    assert response.status_code == 400

    msg = response.get_json().get('msg', False)
    assert msg == 'todo data is not valid'


def test_edit_todo_notfound(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.put(
        '/api/v1/todo/100',
        headers={'Authorization': f'Bearer {token}'},
        json={'text': '123'}
    )

    assert response.status_code == 404

    msg = response.get_json().get('msg', False)
    assert msg == 'todo 100 not found'


def test_edit_todo_mimetype_error(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.put(
        '/api/v1/todo/1',
        headers={'Authorization': f'Bearer {token}'},
        data={'text1': '123'}
    )

    assert response.status_code == 400

    msg = response.get_json().get('msg', False)
    assert msg == 'mimetype is not valid'


def test_delete_todo(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.delete(
        '/api/v1/todo/1',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200

    msg = response.get_json().get('msg', False)
    assert msg == 'todo has been deleted'


def test_delete_todo_notfound(application):
    test_client = application.test_client()

    token = get_jwt(test_client, 'test')
    response = test_client.delete(
        '/api/v1/todo/100',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404

    msg = response.get_json().get('msg', False)
    assert msg == 'todo 100 not found'


def test_delete_todo_without_jwt(application):
    test_client = application.test_client()

    response = test_client.delete(
        '/api/v1/todo/1'
    )

    assert response.status_code == 401

    msg = response.get_json().get('msg', False)
    assert msg == 'Missing Authorization Header'

