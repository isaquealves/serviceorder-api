import base64
import json
import logging
import urllib
from json import JSONDecodeError
from typing import Any, ByteString

from decouple import config
from marshmallow import ValidationError

from app.api.messages import ACTIVATED_ACCOUNT
from app.api.responses import (bad_request_response, created_response,
                               invalid_data_response, no_content_response)
from app.helpers import decode_user_identification, decrypt
from app.models.schemas.user import UserSchema
from app.models.user import User
from app.tasks import send_activation_email

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)


def create(body: dict) -> Any:
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
    sep = config('ACTIVATION_CODE_SEPARATOR', default='+')
    activation_key = config('USER_ACTIVATION_KEY_ATTR', default='username')
    encoded_user_ID = code[:code.index(sep)].encode()
    cyphered_data = urllib.parse.unquote_to_bytes(code[code.index(sep)+1:])
    identity_key = decode_user_identification(encoded_user_ID)

    user = User.where('public_key', '=', identity_key).first_or_fail()
    userData = json.loads(decrypt(user.private_key, cyphered_data))

    activationSubject = User.where(
        activation_key,
        '=',
        userData[activation_key]
    ).first_or_fail()

    if user.to_json() == activationSubject.to_json():
        user.active = True
        user.save()
        return no_content_response('User', message=ACTIVATED_ACCOUNT)
    return bad_request_response(
            'User',
            'Requests data is not recognized'
        )
