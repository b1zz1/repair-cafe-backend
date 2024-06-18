import pytest
from database import db

def test_user_create(user1):
    """
    Testar a criação de um usuário no banco
    Inserir o usuário, e após ler o usuário do BD
    comparar se o conteúdo do usuário lido do BD é o mesmo dos parâmetros da função
    """
    # Criar o usuário no DB
    db.user_create(**user1)

    # Ler o usuário do DB
    user = db.user_read(user_id=1)

    # Comparar os dados do usuário
    assert user.name == user1["name"]
    assert user.email == user1["email"]
    assert user.password == user1["password"]
    assert user.birth_date == user1["birth_date"]

def test_read_all_tasks(user1, user2):
    """
    Criar 2 usuários no BD
    Ler todos os usuários do BD
    Contar quantos usuários retornam
    Testar 1 campo de cada usuário se é idêntico ao enviado
    """
    # Criar 2 usuários
    db.user_create(**user1)
    db.user_create(**user2)

    # Ler usuários do BD
    users = db.user_read(id)
    assert len(users) == 2
    assert users[0].name == user1["name"]
    assert users[1].name == user2["name"]
