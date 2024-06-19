import pytest
from utils.security import generate_salt, hash_password
import pytest
import mariadb

@pytest.fixture(scope="module")
def db_connection():
    conn = mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="pac_test"
    )
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


# Fixture para limpar o banco de dados antes de cada teste
@pytest.fixture(autouse=True)
def clean_database():
    connection = get_db_connection()  # Use sua função get_db_connection() ou outra maneira de obter a conexão
    cursor = connection.cursor()
    cursor.execute("DELETE FROM services")
    connection.commit()
    connection.close()