from unittest.mock import patch, MagicMock, call
import pytest
import mariadb
from datetime import datetime
from database.db import user_read, service_create, service_read, service_update, service_delete, create_connection, \
    user_create, user_update, user_delete

# Teste para criar usuário com falha de conexão
def test_user_create_error():
    with patch('database.db.create_connection', return_value=None):
        with pytest.raises(ValueError, match="Connection failed, test cannot proceed"):
            user_create("Joãozinho", "Silva", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01")
def test_user_read_database_error():
    with patch('database.db.create_connection', side_effect=mariadb.Error("Connection failed")):
        with pytest.raises(mariadb.Error, match="Connection failed"):
            user_read(1)  # Ajuste para um ID válido ou mocke o retorno de user_read


def test_service_create_error():
    with patch('database.db.create_connection', return_value=None):
        with pytest.raises(ValueError, match="Connection failed, test cannot proceed"):
            service_create("Serviço de Reparo", "reparo@example.com", "Descrição do serviço de reparo", "123456789")


# Testes para criação de usuário no Banco de Dados
def test_user_create(db_connection):
    result = user_create("Joãozinho", "Silva", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01")
    assert result == {"message": "User created successfully"}

    conn = db_connection
    with conn.cursor() as cur:
        cur.execute("SELECT name, surname, email, password, salt, birth_date FROM users WHERE email = ?",
                    ("joaozinho@example.com",))
        user = cur.fetchone()
        birth_date = datetime.strptime("2005-01-01", "%Y-%m-%d").date()
        assert user == ("Joãozinho", "Silva", "joaozinho@example.com", "hashedpassword", "salt", birth_date)

# Teste para ler usuário do Banco de Dados
def test_user_read(db_connection):
    conn = db_connection
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, surname, email, password, salt, birth_date) VALUES (?, ?, ?, ?, ?, ?)",
            ("Joãozinho", "Silva", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01"))
        conn.commit()
        cur.execute("SELECT LAST_INSERT_ID()")
        user_id = cur.fetchone()[0]

    result = user_read(user_id)
    result_converted = (
        result['name'], result['surname'], result['email'], result['password'], result['salt'], result['birth_date'])
    assert result_converted == ("Joãozinho", "Silva", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01")

# Teste para atualizar usuário no Banco de Dados
def test_user_update(db_connection):
    conn = db_connection
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, surname, email, password, salt, birth_date) VALUES (?, ?, ?, ?, ?, ?)",
            ("Joãozinho", "Silva", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01"))
        conn.commit()
        cur.execute("SELECT LAST_INSERT_ID()")
        user_id = cur.fetchone()[0]

    result = user_update(user_id, "João", "Souza", "joaozinho_updated@example.com", "newpassword", "2005-01-01")
    assert result == {"message": "User updated successfully"}

    with conn.cursor() as cur:
        cur.execute("SELECT name, surname, email FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        assert user == ("João", "Souza", "joaozinho_updated@example.com")

# Teste para deletar usuário do Banco de Dados
def test_user_delete(db_connection):
    conn = db_connection
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, surname, email, password, salt, birth_date) VALUES (?, ?, ?, ?, ?, ?)",
            ("Joãozinho", "Silva", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01"))
        conn.commit()
        cur.execute("SELECT LAST_INSERT_ID()")
        user_id = cur.fetchone()[0]

    result = user_delete(user_id)
    assert result == {"message": "User soft deleted successfully"}

    with conn.cursor() as cur:
        cur.execute("SELECT is_active FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        assert user[0] == 0

# Teste para criar serviço no Banco de Dados
# No arquivo tests/test_db.py

from unittest.mock import patch, MagicMock, call
import pytest
import mariadb
from database.db import service_create, create_connection

@pytest.mark.usefixtures("clean_database")
def test_service_create():
    # Mock create_connection para retornar um objeto de conexão simulado
    mock_conn = MagicMock(spec=mariadb.connection)
    mock_cursor = mock_conn.cursor.return_value

    with patch('database.db.create_connection', return_value=mock_conn):
        result = service_create("Serviço de Reparo", "reparo@example.com", "Descrição do serviço de reparo", "123456789")
        assert result == {"message": "Service created successfully"}

        # Verificar se a função execute foi chamada com os parâmetros corretos
        expected_query = "INSERT INTO services (name, email, description, phone) VALUES (?, ?, ?, ?)"
        expected_params = ("Serviço de Reparo", "reparo@example.com", "Descrição do serviço de reparo", "123456789")
        mock_cursor.execute.assert_called_once_with(expected_query, expected_params)

        # Verificar se o commit foi chamado no objeto de conexão simulado
        mock_conn.commit.assert_called_once()

        # Verificar se os dados podem ser lidos corretamente
        mock_cursor.fetchone.return_value = ("Serviço de Reparo", "reparo@example.com", "Descrição do serviço de reparo", "123456789")
        # Aqui você deve ajustar conforme existir a função service_read ou similar
        service = service_read("reparo@example.com")
        assert service == ("Serviço de Reparo", "reparo@example.com", "Descrição do serviço de reparo", "123456789")
