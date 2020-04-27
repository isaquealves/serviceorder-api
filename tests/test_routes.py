import json
import pytest
from orator.exceptions.query import QueryException


def test_root(client):
    response = client.get('/v1/')

    expected = {
        'message': 'Welcome to Service order api'
    }
    assert expected == response.json  # nosec


def test_users_create(client):
    user_data = {
        'username': 'Username'
    }
    
    response = client.post(
        '/v1/users',
        content_type='application/json',
        json=json.dumps(user_data))
    result = json.loads(response.json['data'])

    assert response.status_code == 201  # nosec
    assert result['username'] == 'Username'  # nosec
    assert result['id'] == 1  # nosec

    with(pytest.raises(QueryException)) as exc:
        response = client.post(
            '/v1/users',
            content_type='application/json',
            json=json.dumps(user_data))
        assert 'UNIQUE constraint failed' in exc.value  # nosec


@pytest.mark.parametrize('value, expected', (
    ['user', 422],
    ['john.connor', 201],
    ['bilbo-baggins', 422],
    ['harry_potter', 201],
    ['peter-parker', 201],
    ['sarum@n', 422],
    ['super.sayajin#4', 422]
))
def test_create_user_invalid_username(client, value, expected):
    user_data = {
        'username': value
    }
    response = client.post(
        '/v1/users',
        content_type='application/json',
        json=json.dumps(user_data))
    
    assert response.status_code == expected

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

