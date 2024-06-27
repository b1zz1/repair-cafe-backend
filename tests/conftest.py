from socket import create_connection

import pytest
import mariadb
from datetime import datetime

@pytest.fixture(scope="module")
def db_connection():
    conn = create_connection()
    if conn is None:
        pytest.fail("Database connection could not be established.")
    yield conn
    conn.close()

def get_db_connection():
    return mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="pac_test"
    )

@pytest.fixture(scope="module")
def db_connection():
    conn = get_db_connection()
    yield conn
    conn.close()

@pytest.fixture(autouse=True)
def clean_database():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM services")
    connection.commit()
    connection.close()

@pytest.fixture
def db_setup_teardown():
    # Configuração antes do teste
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE email = ?", ("joaozinho@example.com",))
            conn.commit()
    yield
    # Limpeza após o teste
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE email = ?", ("joaozinho@example.com",))
            conn.commit()
