import base64
import json
import urllib

import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from decouple import config

from app.helpers import (decode_user_identification, decrypt,
                         encode_user_identification, encrypt_data,
                         generate_auth_code, store_user_auth_code)

from app.providers.redis import redisClient
from app.models.user import User

pytest.key_test = ''


def test_encrypt_data(db_scope_fn):
    user_data = {
        'username': 'Username',
        'first_name': 'User',
        'last_name': 'Last',
        'email': config('ACTIVATION_EMAIL_TESTING', 'mail@example.com')
    }

    user = User.create(user_data)
    key = serialization.load_pem_private_key(
        user.private_key,
        password=None,
        backend=default_backend()
    )

    cyphered = urllib.parse.unquote_to_bytes(encrypt_data(user))
    uncyphered = key.decrypt(
        cyphered,
        padding.OAEP(
             mgf=padding.MGF1(algorithm=hashes.SHA256()),
             algorithm=hashes.SHA256(),
             label=None
         )
    )
    assert cyphered is not None  # nosec
    assert cyphered != ''  # nosec
    assert user.email == json.loads(uncyphered)['email']  # nosec


def test_decrypt(db_scope_fn):
    user_data = {
        'username': 'Username',
        'first_name': 'User',
        'last_name': 'Last',
        'email': config('ACTIVATION_EMAIL_TESTING', 'mail@example.com')
    }

    user = User.create(user_data)
    cyphered = encrypt_data(user)
    pytest.key_test = user.public_key
    decrypted = json.loads(decrypt(user.private_key, cyphered))
    
    assert user.email == decrypted['email']  # nosec


def test_encode_user_identification():
    encoded_id = encode_user_identification(pytest.key_test)
    mid_str = round(len(encoded_id) / 2)
    assert encoded_id[mid_str - 1:-1] == base64.urlsafe_b64encode(
        pytest.key_test
    )[:mid_str]


def test_decode_user_identification():
    encoded_id = encode_user_identification(pytest.key_test)
    decoded = decode_user_identification(encoded_id)
    assert decoded == pytest.key_test


def test_generate_auth_code():
    token = generate_auth_code()
    assert token is not None


def test_store_user_auth_code(client):
    store_user_auth_code('user', generate_auth_code(), 10)
    assert redisClient.get('user') is not None