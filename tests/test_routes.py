import json
from unittest.mock import patch

import pytest
from decouple import config
from orator.exceptions.query import QueryException

from app.models.user import User
from app.helpers import (
    encrypt_data,
    encode_user_identification,
    decrypt,
    decode_user_identification,
    generate_auth_code,
    store_user_auth_code
)

pytest.user = None
pytest.code = None


def test_root(client, db):
    response = client.get('/v1/')

    expected = {
        'message': 'Welcome to Service order api'
    }
    assert expected == response.json  # nosec


def test_users_create(client):
    user_data = {
        'username': 'Username',
        'first_name': 'User',
        'last_name': 'Last',
        'email': config('ACTIVATION_EMAIL_TESTING', 'mail@example.com')
    }

    response = client.post(
        '/v1/users',
        content_type='application/json',
        json=json.dumps(user_data))
    result = json.loads(response.json['data'])

    assert response.status_code == 201  # nosec
    assert result['username'] == 'Username'.lower()  # nosec
    assert result['id'] == 1  # nosec
    pytest.user = User.find(result['id'])
    with(pytest.raises(QueryException)) as exc:
        response = client.post(
            '/v1/users',
            content_type='application/json',
            json=json.dumps(user_data))
        assert 'UNIQUE constraint failed' in exc.value  # nosec


@pytest.mark.parametrize('username, first, last, email, expected', (
    ['user', 'User', 'Name', 'email@example.com', 422],
    ['john.connor', 'John', 'Connor', 'john@terminat.or', 201],
    ['bilbo-baggins', 'Bilbo', 'Baggins', 'bilbo@coun.ty', 422],
    ['peter-parker', 'Peter', 'Parker', 'peter@dailyplan.et', 201],
    ['sarum@n', 'Saruman', '', 'saru.man-the-white@middleearth.net', 422],
    ['super.sayajin#4', '', '', '', 422]
))
def test_create_user_invalid_username(
    client,
    username,
    first,
    last,
    email,
    expected
):
    with patch('app.api.user.send_activation_email.apply_async') as task:
        user_data = {
            'username': username,
            'first_name': first,
            'last_name': last,
            'email': email
        }
        response = client.post(
            '/v1/users',
            content_type='application/json',
            json=json.dumps(user_data))

        assert response.status_code == expected  # nosec
        assert task.called_once()

def test_account_activation(client):
    code = encrypt_data(pytest.user)
    user_id = encode_user_identification(pytest.user.pub_key)
    link = ''.join([
        f'/{config("API_VERSION", "v1")}/',
        f'users/activate/'
    ])
    query = {
        'code': f'{user_id.decode()}+{code}'
    }
    
    response = client.get(link, query_string=query, content_type='application/json')
    assert response.status_code == 204

@pytest.mark.parametrize(
    'username, expect',
    (
        ['username', 'A code has been sent to your email.'],
        [
            config('ACTIVATION_EMAIL_TESTING', 'mail@example.com'),
            'A code has been sent to your email.'
        ],
        ['test', "This user doesn't exist."],
        ['ἰsaquealves@gmaἰl.com', "This user doesn't exist."]
    )
)
def test_auth(client, username, expect):
    data = {
        'username': username
    }
    response = client.post(
        '/v1/auth',
        content_type='application/json',
        json=json.dumps(data)
    )

    result = response.json

    assert expect in result['message']  # nosec


def test_token_emission(client):
    code = generate_auth_code()
    uid = '1'
    store_user_auth_code(code, f'{code-uid}', 120)
    data = {
        'code':  code
    }
    response = client.post(
        '/v1/auth/token',
        content_type='application/json',
        json=json.dumps(data)
    )
    response_data = response.json.keys()
    assert all(lambda x: x in response_data for x in ['token', 'refresh'])


