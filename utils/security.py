import hashlib
import secrets


def hash_password(password, salt):
    hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
    return hashed_password


def generate_salt():
    return secrets.token_hex(16)