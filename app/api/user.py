import json
from json import JSONDecodeError
import logging
from app.models.user import User
from flask import jsonify

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)


def create(body: dict):
    try:
        data = json.loads(body)
        user = User.create(data)
        response = jsonify(user.to_json())
        response.status_code = 201
        return response
    except JSONDecodeError as decodeError:
        LOGGER.critical(f'Error when decoding provided data: {decodeError}')
        LOGGER.critical(f'Provided data: {data}')
    return {'status_code': 400, 'data': body}
