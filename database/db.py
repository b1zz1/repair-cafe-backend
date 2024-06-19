# para as funções relacionadas ao database, utilize o padrão snake case
# considere para nomenclatura a tabela a ser afetada e o comando. Por exemplo, criar usuário: def user_create()
from contextlib import contextmanager

import mariadb
from flask import jsonify


def create_connection():
    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="pac_test"
        )
        return conn
    except mariadb.Error as err:
        print(f"Error connecting to MariaDB: {err}")
        return 1

@contextmanager
def get_db_connection():
    conn = create_connection()
    try:
        yield conn
    finally:
        if conn:
            conn.close()


# manipulação de usuário
def user_create(name, email, password, salt, birth_date):
    query = "INSERT INTO users(name, email, password, salt, birth_date) VALUES (?, ?, ?, ?, ?)"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (name, email, password, salt, birth_date))
                conn.commit()
                print("User created successfully")
                return {"message": "User created successfully"}
            except mariadb.Error as err:
                print(f"Error: {err}")
                return {"error": str(err)}, 500
        else:
            return {"error": "Database connection failed"}, 500


def user_read(id):
    query = "SELECT name, email, password, salt, birth_date FROM users WHERE id = ?"

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(query, (id,))
            data = cur.fetchone()
            return data
        except mariadb.Error as err:
            print(f"Error: {err}")
            return None, 500


def user_update(id, name, email, password, birth_date):
    query = "UPDATE users SET name = COALESCE(?, name), email = COALESCE(?, email), password = COALESCE(?, password), birth_date = COALESCE(?, birth_date) WHERE id = ?"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (name, email, password, birth_date, id))
                conn.commit()
                return {"message": "User updated successfully"}
            except mariadb.Error as err:
                print(f"Error: {err}")
                return {"error": str(err)}
        else:
            return {"error": "Database connection failed"}, 500


def user_delete(id):
    query = "UPDATE users SET is_active = 0 WHERE id = ?"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (id,))
                conn.commit()
                return {"message": "User soft deleted successfully"}
            except mariadb.Error as err:
                print(f"Error: {err}")
                return {"error": str(err)}
        else:
            return {"error": "Database connection failed"}, 500


# manipulação de serviços
def service_create(name, email, description, phone):
    query = "INSERT INTO services(name, email, description, phone) VALUES (?, ?, ?, ?)"

    with get_db_connection() as conn:
        if conn:
            try:
                # Verifica se o email já existe
                cur = conn.cursor()
                cur.execute("SELECT id FROM services WHERE email = ?", (email,))
                existing_service = cur.fetchone()
                if existing_service:
                    return {"error": f"O email '{email}' já está sendo utilizado por outro serviço"}, 409

                # Se o email não existir, cria o serviço
                cur.execute(query, (name, email, description, phone))
                conn.commit()

                # Recupera o ID do serviço criado
                service_id = cur.lastrowid

                print("Service created successfully with ID:", service_id)
                return service_id  # Retorna o ID do serviço criado
            except mariadb.Error as err:
                print(f"Error: {err}")
                return {"error": str(err)}, 500
        else:
            return {"error": "Database connection failed"}, 500


def service_read(id):
    query = "SELECT id, name, email, description, phone FROM services WHERE id = ?"

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(query, (id,))
            data = cur.fetchone()
            return data  # Retorna os dados do serviço ou None se não encontrado
        except mariadb.Error as err:
            print(f"Error: {err}")
            return None


def service_read_all():
    query = "SELECT id, name, email, description, phone FROM services WHERE is_active = 1"

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return data
        except mariadb.Error as err:
            print(f"Error: {err}")
            return {"error": str(err)}, 500


# Atualização da função service_update para retornar -1 em caso de erro
def service_update(id, name, email, description, phone):
    query = "UPDATE services SET name = COALESCE(?, name), email = COALESCE(?, email), description = COALESCE(?, description), phone = COALESCE(?, phone) WHERE id = ?"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (name, email, description, phone, id))
                conn.commit()

                if cur.rowcount == 0:
                    return 0  # Retorna 0 se nenhum serviço foi atualizado

                print("Service updated successfully")
                return cur.rowcount  # Retorna o número de linhas atualizadas
            except mariadb.Error as err:
                print(f"Error: {err}")
                return -1  # Retorna -1 em caso de erro de banco de dados
        else:
            return -1  # Retorna -1 se a conexão com o banco de dados falhar


# Atualização da função service_delete para retornar -1 em caso de erro
def service_delete(id):
    query = "UPDATE services SET is_active = 0 WHERE id = ?"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (id,))
                conn.commit()
                return cur.rowcount  # Retorna o número de linhas afetadas
            except mariadb.Error as err:
                print(f"Error: {err}")
                return -1  # Retorna -1 em caso de erro
        else:
            return -1  # Retorna -1 se a conexão falhar

