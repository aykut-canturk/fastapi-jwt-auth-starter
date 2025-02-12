from base64 import urlsafe_b64encode
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from app.config import settings

if not settings.crypto_secret:
    raise ValueError("CryptoSecret is not set in the environment variables.")
s = bytes(settings.crypto_secret, "utf-8")
key = urlsafe_b64encode(s)

fernet = Fernet(key)


def encrypt(message: str):
    enc_message = fernet.encrypt(message.encode()).decode("utf-8")
    return enc_message


def decrypt(enc_message: str):
    dec_message = fernet.decrypt(enc_message).decode()
    return dec_message


def hash_password(password: str):
    hashed_password = generate_password_hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str):
    return check_password_hash(hashed_password, password)
