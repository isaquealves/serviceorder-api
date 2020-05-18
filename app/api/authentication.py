import json
import logging
from typing import Any
from flask import jsonify
from app.api.responses import not_found_response, response_ok
from app.models.user import User
from app.tasks import send_authentication_code
from app.providers.redis import redisClient
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


def request(body: Any):
    try:
        username = json.loads(body)["username"]
        user = User.where_raw(
            "username=? or email=?", [username, username]
        ).first()
        if user:
            send_authentication_code.apply_async((user,))
            return response_ok(
                message="A code has been sent to your email.\
                Please, use the code to confirm your access",
            )
    except ModuleNotFoundError as modelError:
        LOGGER.error(modelError)
    except json.JSONDecodeError as jsonError:
        LOGGER.error(jsonError)
    return not_found_response("Auth", description="user")


def token(body: Any):
    try:
        code = json.loads(body)["code"].encode()
        stored_code, userid = redisClient.get(code).decode().split("-")
        user = User.find(userid)
        if not stored_code == code:
            return not_found_response("Auth", description="user")

        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)

        return jsonify({"token": access_token, "refresh": refresh_token})
    except ModuleNotFoundError as modelError:
        LOGGER.error(modelError)
    except json.JSONDecodeError as jsonError:
        LOGGER.error(jsonError)
    return not_found_response("Auth", description="user")


@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity)
    refresh_token = create_refresh_token(identity)
    return jsonify({"token": access_token, "refresh": refresh_token})
