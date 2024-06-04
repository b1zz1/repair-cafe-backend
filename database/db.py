# para as funções relacionadas ao database, utilize o padrão snake case
# considere para nomenclatura a tabela a ser afetada e o comando. Por exemplo, criar usuário: def user_create()

import mariadb

def create_connection():
    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database="n2_database"
        )
    except mariadb.Error as err:
        print(f"Error connecting to MariaDB: {err}")

    cur = conn.cursor()


# manipulação de usuário
def user_create():
    pass


def user_read():
    pass


def user_update():
    pass


def user_delete():
    pass
