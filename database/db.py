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
def user_create(name, surname, email, password, salt, birth_date):
    query = "INSERT INTO users(name, surname, email, password, salt, birth_date) VALUES (?, ?, ?, ?, ?, ?)"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (name, surname, email, password, salt, birth_date))
                conn.commit()
                print("User created successfully")
                return {"message": "User created successfully"}
            except mariadb.Error as err:
                print(f"Error: {err}")
                return {"error": str(err)}, 500
        else:
            return {"error": "Database connection failed"}, 500


def user_read(id):
    query = "SELECT name, email, password, salt, creation_date FROM users WHERE id = ?"

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(query, (id,))
            data = cur.fetchone()
            return data
        except mariadb.Error as err:
            print(f"Error: {err}"), 500


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
                cur = conn.cursor()
                cur.execute(query, (name, email, description, phone))
                conn.commit()
                print("Service created successfully")
                return {"message": "Service created successfully"}
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
            data = cur.fetchall()
            return data
        except mariadb.Error as err:
            print(f"Error: {err}")
            return {"error": str(err)}, 500


def service_read_all_by_expertise():
    query = """
    SELECT services.id, services.name, services.email, services.description, services.phone, services.owner_id, expertises.name, expertises.description
    FROM services_expertises 
    JOIN services ON services_expertises.service_id  = services.id
    JOIN expertises ON services_expertises.expertise_id = expertises.id 
    """

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return data
        except mariadb.Error as err:
            print(f"Error: {err}")
            return {"error": str(err)}, 500


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


def service_update(id, name, email, description, phone):
    query = "UPDATE services SET name = COALESCE(?, name), email = COALESCE(?, email), description = COALESCE(?, description), phone = COALESCE(?, phone) WHERE id = ?"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (name, email, description, phone, id))
                conn.commit()
                if cur.rowcount == 0:
                    return {"error": "Service not found"}, 404
                print("Service updated successfully")
                return {"message": "Service updated successfully"}
            except mariadb.Error as err:
                print(f"Error: {err}")
                return {"error": str(err)}, 500
        else:
            return {"error": "Database connection failed"}, 500


def service_delete(id):
    query = "UPDATE services SET is_active = 0 WHERE id = ?"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (id,))
                conn.commit()
                return {"message": "Service soft deleted successfully"}
            except mariadb.Error as err:
                print(f"Error: {err}")
                return {"error": str(err)}
        else:
            return {"error": "Database connection failed"}, 500


# manipulação de expertise
def expertise_read_all():
    query = "SELECT id, name, description FROM services"

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return data
        except mariadb.Error as err:
            print(f"Error: {err}")
            return {"error": str(err)}, 500
