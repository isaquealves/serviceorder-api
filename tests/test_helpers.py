import urllib
import json
import pytest
import base64
from decouple import config
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from app.models.user import User
from app.helpers import encrypt_data, decrypt, encode_user_identification, decode_user_identification

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
    assert base64.urlsafe_b64decode(decoded) == pytest.key_test

