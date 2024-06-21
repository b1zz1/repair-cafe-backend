from flask import Blueprint, request
from database.db import *
from utils.security import hash_password, generate_salt

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user/create', methods=['POST'])
def userCreate():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    birth_date = data.get('birth_date')
    salt = generate_salt()
    password = hash_password(data.get('password'), salt)

    response = user_create(name, surname, email, password, salt, birth_date )

    return jsonify(response)


@user_bp.route('/user/read/<int:id>', methods=['GET'])
def userRead(id):
    user = user_read(id)

    return jsonify(user)


@user_bp.route('/user/update/<int:id>', methods=['PUT'])
def userUpdate(id):
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    birth_date = data.get('birth_date')
    salt = generate_salt()
    password = hash_password(data['password'], salt)

    response = user_update(id, name, surname, email, password, birth_date)

    return jsonify(response)


@user_bp.route('/user/delete', methods=['PATCH'])
def userDelete():
    data = request.get_json()
    id = data.get('id')

    response = user_delete(id)

    return jsonify(response)
