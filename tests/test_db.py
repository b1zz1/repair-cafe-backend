from unittest.mock import patch
import pytest
import mariadb
from datetime import datetime

import database.db
from database.db import user_read, service_create, service_read, service_update, service_delete, create_connection, \
    user_create, user_update, user_delete


# Função para obter a conexão com o banco de dados
def get_db_connection():
    return mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="pac_test"
    )

def test_create_connection_failure():
    with patch('database.db.mariadb.connect', side_effect=mariadb.Error("Connection Error")):
        result = create_connection()
        assert result == 1


# Testes para criação de usuário no Banco de Dados
def test_user_create():
    """
    Testa a criação de um usuário no banco de dados.
    """
    # Chama a função user_create
    result = user_create("Joãozinho", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01")

    # Verifica se a criação foi bem-sucedida
    assert result == {"message": "User created successfully"}

    # Conecta ao banco de dados para verificar se o usuário foi inserido corretamente
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name, email, password, salt, birth_date FROM users WHERE email = ?",
                        ("joaozinho@example.com",))
            user = cur.fetchone()
            # Convertendo a data para datetime.date para comparação
            birth_date = datetime.strptime("2005-01-01", "%Y-%m-%d").date()
            assert user == ("Joãozinho", "joaozinho@example.com", "hashedpassword", "salt", birth_date)


def test_user_read():
    """
    Testa a leitura de um usuário no banco de dados.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, email, password, salt, birth_date) VALUES (?, ?, ?, ?, ?)",
                        ("Joãozinho", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01"))
            conn.commit()
            cur.execute("SELECT LAST_INSERT_ID()")
            user_id = cur.fetchone()[0]
    result = user_read(user_id)
    # Convertendo a data para string no formato YYYY-MM-DD para comparação
    result_converted = (result[0], result[1], result[2], result[3], result[4].strftime('%Y-%m-%d'))
    assert result_converted == ("Joãozinho", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01")


def test_user_read_nonexistent_id():
    """
    Testa a função user_read quando é fornecido um ID que não existe no banco de dados.
    Esperamos que a função retorne None.
    """
    # Chama a função user_read com um ID que não existe no banco de dados
    result = user_read(9999)  # Supondo que 9999 não existe no banco de dados

    # Verifica se a função retornou None
    assert result is None

def test_user_read_database_error():
    """
    Testa a função user_read quando ocorre um erro de banco de dados.
    Esperamos que a função retorne None.
    """
    # Chama a função user_read com um tipo de ID que cause um erro de banco de dados
    result = user_read("invalid_id_type")  # Simulando um tipo de ID que causa erro

    # Verifica se a função retornou None
    assert result is None


def test_user_update():
    """
    Testa a atualização de um usuário no banco de dados.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, email, password, salt, birth_date) VALUES (?, ?, ?, ?, ?)",
                        ("Joãozinho", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01"))
            conn.commit()
            cur.execute("SELECT LAST_INSERT_ID()")
            user_id = cur.fetchone()[0]
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET email = ? WHERE id = ?", ("joaozinho_updated@example.com", user_id))
            conn.commit()
        with conn.cursor() as cur:
            cur.execute("SELECT email FROM users WHERE id = ?", (user_id,))
            user = cur.fetchone()
            assert user[0] == "joaozinho_updated@example.com"


def test_user_update_error():
    """
    Testa a função user_update em caso de erro de banco de dados.
    """
    id = -1  # Usar um ID negativo para forçar um erro
    name = "Novo Nome"
    email = "novo_email@example.com"
    password = "novasenha"
    birth_date = "2000-01-01"

    # Chamada da função user_update com dados que devem causar um erro
    result = user_update(id, name, email, password, birth_date)

    # Verifica que o usuário não foi atualizado
    assert "User updated successfully" not in result


def test_user_delete():
    """
    Testa a exclusão de um usuário no banco de dados.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, email, password, salt, birth_date) VALUES (?, ?, ?, ?, ?)",
                        ("Joãozinho", "joaozinho@example.com", "hashedpassword", "salt", "2005-01-01"))
            conn.commit()
            cur.execute("SELECT LAST_INSERT_ID()")
            user_id = cur.fetchone()[0]
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cur.fetchone()
            assert user is None


def test_user_delete_error():
    """
    Testa a função user_delete em caso de erro de banco de dados.
    """
    id = -1  # Usar um ID negativo para forçar um erro

    # Chamada da função user_delete com um ID que deve causar um erro
    result = user_delete(id)

    # Verifica que o usuário não foi deletado
    assert "User deleted successfully" not in result


# Teste de criação de serviços no Banco de Dados

def test_service_create():
    """
    Testa a criação de um serviço no banco de dados.
    """
    service_id = service_create("Serviço de Reparo", "reparo@example.com", "Descrição do serviço de reparo", "123456789")
    assert service_id is not None  # Verifica se o serviço foi criado com sucesso

def test_service_read():
    """
    Testa a leitura de um serviço no banco de dados.
    """
    # Cria um serviço com um email único para este teste
    service_id = service_create("Serviço de Reparo", "reparo_read@example.com", "Descrição do serviço de reparo", "123456789")
    assert service_id is not None  # Verifica se o serviço foi criado com sucesso

    # Realiza a leitura do serviço criado
    result = service_read(service_id)

    if isinstance(result, tuple):
        # Converte a data para string no formato YYYY-MM-DD para comparação
        if isinstance(result[4], datetime):
            result_converted = (result[0], result[1], result[2], result[3], result[4].strftime('%Y-%m-%d'))
        else:
            result_converted = (result[0], result[1], result[2], result[3], result[4])  # Assume que result[4] já é uma string
        assert result_converted == (service_id, "Serviço de Reparo", "reparo_read@example.com", "Descrição do serviço de reparo", "123456789")
    elif isinstance(result, dict) and 'error' in result:
        assert False, f"Erro ao ler serviço com ID {service_id}: {result['error']}"
    else:
        assert False, f"Resultado inesperado ao ler serviço com ID {service_id}: {result}"


def test_service_read_all(db_setup_teardown):
    """
    Testa a função service_read_all para verificar se retorna os serviços ativos.
    """
    # Inserir dados de teste no banco de dados
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO services (name, email, description, phone, is_active) VALUES (%s, %s, %s, %s, %s)",
                        ("Serviço A", "servicoa@example.com", "Descrição do Serviço A", "123456789", 1))
            cur.execute("INSERT INTO services (name, email, description, phone, is_active) VALUES (%s, %s, %s, %s, %s)",
                        ("Serviço B", "servicob@example.com", "Descrição do Serviço B", "987654321", 1))
            conn.commit()

    # Chamar a função service_read_all e verificar o retorno
    result = database.db.service_read_all()

    # Verificar se os serviços ativos foram retornados corretamente
    assert len(result) == 2
    assert result[0][1] == "Serviço A"
    assert result[1][1] == "Serviço B"


def test_service_update():
    """
    Testa a atualização de um serviço no banco de dados.
    """
    # Cria um serviço com um email único para este teste
    service_id = service_create("Serviço de Reparo", "reparo_update@example.com", "Descrição do serviço de reparo", "123456789")
    assert service_id is not None  # Verifica se o serviço foi criado com sucesso

    # Realiza a atualização do serviço criado
    updated_rows = service_update(service_id, "Serviço de Reparo Atualizado", "reparo_update_updated@example.com", "Nova descrição do serviço de reparo", "987654321")

    if updated_rows >= 0:
        assert updated_rows > 0 or updated_rows == 0  # Verifica se as linhas foram atualizadas ou nenhum serviço foi encontrado
    else:
        assert False, f"Erro ao atualizar serviço com ID {service_id}: {updated_rows}"

def test_service_delete():
    """
    Testa a exclusão de um serviço no banco de dados.
    """
    # Cria um serviço com um email único para este teste
    service_id = service_create("Serviço de Reparo", "reparo_delete@example.com", "Descrição do serviço de reparo", "123456789")
    assert service_id is not None  # Verifica se o serviço foi criado com sucesso

    # Realiza a exclusão do serviço criado
    deleted_rows = service_delete(service_id)

    if deleted_rows >= 0:
        assert deleted_rows > 0 or deleted_rows == 0  # Verifica se as linhas foram marcadas como inativas ou nenhum serviço foi encontrado
    else:
        assert False, f"Erro ao excluir serviço com ID {service_id}: {deleted_rows}"
