import json
import logging
from json import JSONDecodeError
from marshmallow import ValidationError

from app.models.user import User
from app.models.schemas.user import UserSchema
from app.api.responses import (
    bad_request_response,
    invalid_data_response,
    created_response
)
from app.tasks import send_activation_email


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)


def create(body: dict):
    try:
        data = UserSchema().load(json.loads(body))
        user = User.create(data)
        send_activation_email.apply_async((user,))
        return created_response('User', data=user.to_json())
    except ValidationError as errors:
        return invalid_data_response('User', errors=errors.messages)
    except JSONDecodeError as decodeError:
        LOGGER.critical(f'Error when decoding provided data: {decodeError}')
        LOGGER.critical(f'Provided data: {json.loads(body)}')
        return bad_request_response(
            'User',
            'Data provided is not serializable'
        )


def activate(code):
    ...
