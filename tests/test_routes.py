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
        'username': 'Username',
        'first_name': 'User',
        'last_name': 'Last',
        'email': 'mail@example.com'
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
