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


def user_read():
    query = "SELECT name, email, password, salt, creation_date FROM users WHERE id = ?"

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(query, (1,))
            data = cur.fetchone()
            return data
        except mariadb.Error as err:
            print(f"Error: {err}"), 500


def user_update():
    pass


def user_delete():
    pass


# Service database

# funções relacionadas ao database para serviços
def service_create_db(name, email, description, phone):
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


def service_read_db():
    query = "SELECT id, name, email, description, phone FROM services"

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
            return data
        except mariadb.Error as err:
            print(f"Error: {err}")
            return {"error": str(err)}, 500


def service_update_db(service_id, name, email, description, phone):
    query = "UPDATE services SET name = ?, email = ?, description = ?, phone = ? WHERE id = ?"

    with get_db_connection() as conn:
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(query, (name, email, description, phone, service_id))
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


def service_delete_db(service_id):
    pass
