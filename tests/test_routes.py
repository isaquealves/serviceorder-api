import json
import pytest
from orator.exceptions.query import QueryException
from app.models.user import User


def test_root(client):
    response = client.get('/v1/')

    expected = {
        'message': 'Welcome to Service order api'
    }
    assert expected == response.json  # nosec


def test_users_create(client):
    user_data = {
        'username': 'User'
    }
    response = client.post(
        '/v1/users',
        content_type='application/json',
        json=json.dumps(user_data))
    result = json.loads(response.json)
    count = len(User.all())
    assert response.status_code == 201  # nosec
    assert count > 0  # nosec
    assert result['username'] == 'User'  # nosec
    assert result['id'] == 1  # nosec
    with(pytest.raises(QueryException)) as exc:
        response = client.post(
            '/v1/users',
            content_type='application/json',
            json=json.dumps(user_data))
        assert 'UNIQUE constraint failed' in exc.value
        
        


# def test_get_auth(client):
#     response = client.get('/v1/auth')
#     assert response.status == '405 METHOD NOT ALLOWED'

# def test_post_auth(client):
#     login_data = {
#         'username': 'test'
#     }
#     keys = ['access_token', 'refresh_token']
#     expected = {
#         'message' : 'Check your email for our 6 number code'
#     }
#     response = client.post(
#       '/v1/auth', 
#       content_type='application/json',
#       data=login_data)

#     assert response.status_code == 200
#     assert response.json == expected

