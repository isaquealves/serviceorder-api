import json
from decouple import config
from unittest.mock import patch


def test_send_activation_email(client):
    with patch('app.api.user.send_activation_email.apply_async') as task:
        user_data = {
            'username': 'usernametest',
            'first_name': 'User',
            'last_name': 'Last',
            'email': config('ACTIVATION_EMAIL_TESTING', 'mail@example.com')
        }
        
        client.post(
            '/v1/users',
            content_type='application/json',
            json=json.dumps(user_data)
        )

        task.assert_called_once()
    