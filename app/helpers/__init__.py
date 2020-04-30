import logging
import urllib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from app.models.user import User

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.ERROR)


def sign_email(account: User):

    key = serialization.load_pem_private_key(
        account.private_key,
        password=None,
        backend=default_backend()
    )
    info = account.email.encode()

    signedUsername = key.sign(
        data=info,
        padding=padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        algorithm=hashes.SHA256()
    )

    return urllib.parse.quote_from_bytes(signedUsername)

