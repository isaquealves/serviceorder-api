import urllib
from decouple import config
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from app.models.user import User
from app.helpers import encrypt_data, decrypt


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
    assert user.email == uncyphered.decode()  # nosec


def test_decrypt(db_scope_fn):
    user_data = {
        'username': 'Username',
        'first_name': 'User',
        'last_name': 'Last',
        'email': config('ACTIVATION_EMAIL_TESTING', 'mail@example.com')
    }

    user = User.create(user_data)
    cyphered = encrypt_data(user)

    decrypted = decrypt(user.private_key, cyphered)
    
    assert user.email.encode() == decrypted
