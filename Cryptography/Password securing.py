import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password_provided = "SQLShack@Demo"
password = password_provided.encode()
salt = b'SQLShack_'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=200000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
print(key)
