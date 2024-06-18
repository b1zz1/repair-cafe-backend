import pytest
from utils.security import generate_salt, hash_password

@pytest.fixture
def user1():
    """
    Define o user1
    """
    salt = generate_salt()
    user1 = {
        "name": "João",
        "email": "joaozinho@gmail.com",
        "salt": salt,
        "password": hash_password("123456", salt),
        "birth_date": "2004-01-24"
    }
    yield user1

@pytest.fixture
def user2():
    """
    Define o user2
    """
    salt = generate_salt()
    user2 = {
        "name": "Maria",
        "email": "mariazinha@gmail.com",
        "salt": salt,
        "password": hash_password("123456", salt),
        "birth_date": "2015-10-12"
    }
    yield user2
