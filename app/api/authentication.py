import json
from typing import Any

from app.api.responses import not_found_response, response_ok
from app.models.user import User
from app.tasks import send_authentication_code


def request(body: Any):
    username = json.loads(body)['username']
    user = User.where_raw(
        'username=? or email=?',
        [username, username]
    ).first()
    if user:
        send_authentication_code.apply_async((user,))
        return response_ok(
            message='A code has been sent to your email.\
            Please, use the code to confirm your access',
        )
    return not_found_response(
        'Auth',
        description="user"
    )


def token():
    return {}


def refresh():
    ...
