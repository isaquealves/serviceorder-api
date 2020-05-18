import base64
import json
import logging
import secrets
import urllib
from typing import AnyStr, ByteString

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from decouple import config

from app.models.schemas.user import UserSchema
from app.models.user import User
from app.providers.redis import redisClient

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.ERROR)


def encrypt_data(account: User):

    private_key = account.private_key

    key = serialization.load_pem_private_key(
        private_key, password=None, backend=default_backend()
    )

    user = UserSchema(exclude=["public_key", "first_name", "last_name"]).dump(
        account
    )

    cypher = key.public_key().encrypt(
        json.dumps(user).encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return urllib.parse.quote_from_bytes(cypher)


def encode_user_identification(str: ByteString) -> ByteString:
    encoded_str = base64.urlsafe_b64encode(str)
    mid_str = round(len(encoded_str) / 2)
    end = b"".join([chr(encoded_str[-1]).encode()])
    start = encoded_str[:mid_str]
    mid = encoded_str[mid_str:-1]
    result = b"".join([mid, start, end])
    return result


def decode_user_identification(encoded_str: ByteString) -> ByteString:
    # import pudb; pudb.set_trace()
    mid_str = round(len(encoded_str) / 2)
    end = b"".join([chr(encoded_str[-1]).encode()])
    start = encoded_str[: mid_str - 1]
    # fmt: off
    mid_pos = encoded_str[mid_str - 1: -1]
    # fmt: on
    result = b"".join([mid_pos, start, end])
    return base64.urlsafe_b64decode(result)


def decrypt(private_key, encrypted_str: AnyStr) -> AnyStr:
    key = serialization.load_pem_private_key(
        private_key, password=None, backend=default_backend()
    )

    return key.decrypt(
        urllib.parse.unquote_to_bytes(encrypted_str),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def generate_auth_code():
    return secrets.token_hex(3)


def store_user_auth_code(username: AnyStr, auth_code: AnyStr, ttl: int = None):

    if auth_code:
        redisClient.setex(
            username, ttl or config("AUTH_CODE_VALID_UNTIL", 10), auth_code
        )
