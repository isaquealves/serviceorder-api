from unittest.mock import patch

import pytest
from decouple import config


def test_send_activation_email(client):
    with patch("app.api.user.send_activation_email.apply_async") as task:
        user_data = {
            "username": "usernametest",
            "first_name": "User",
            "last_name": "Last",
            "email": config("ACTIVATION_EMAIL_TESTING", "mail@example.com"),
        }

        client.post(
            "/v1/users", content_type="application/json", json=user_data,
        )

        task.assert_called_once()


@pytest.mark.parametrize(
    "username, expected_status",
    (
        [config("ACTIVATION_EMAIL_TESTING", "mail@example.com"), 200],
        ["test", 404],
        ["ἰsaquealves@gmaἰl.com", 404],
    ),
)
def test_send_authentication_code(client, username, expected_status):
    with patch(
        "app.api.authentication.send_authentication_code.apply_async"
    ) as task:
        user_data = {
            "username": username,
        }
        response = client.post(
            "/v1/auth", content_type="application/json", json=user_data,
        )

        assert response.status_code == expected_status
        if response.status_code == 200:
            task.assert_called_once()
