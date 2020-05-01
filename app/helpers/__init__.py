import logging
import urllib
from typing import AnyStr
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from app.models.user import User

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.ERROR)


def encrypt_data(account: User):

    private_key = account.private_key
    
    key = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )
    info = account.email.encode()

    cypher = key.public_key().encrypt(
        info,
        padding.OAEP(
             mgf=padding.MGF1(algorithm=hashes.SHA256()),
             algorithm=hashes.SHA256(),
             label=None
         )
    )

    return urllib.parse.quote_from_bytes(cypher)


def decrypt(private_key, encrypted_str: AnyStr) -> AnyStr:
    key = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )

    return key.decrypt(
        urllib.parse.unquote_to_bytes(encrypted_str),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
