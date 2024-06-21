from flask import Blueprint, request
from database.db import *
from utils.security import hash_password, generate_salt

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user/create', methods=['POST'])
def userCreate():
    data = request.get_json()
    name = data['name']
    surname = data['surname']
    email = data['email']
    salt = generate_salt()
    password = hash_password(data['password'], salt)

    response = user_create(name, surname, email, password, salt, "2005-01-01")

    return jsonify(response)


@user_bp.route('/user/read', methods=['GET'])
def userRead():
    data = request.get_json()
    id = data.get('id')

    user = user_read(id)

    return jsonify(user)


@user_bp.route('/user/update', methods=['PUT'])
def userUpdate():
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    birth_date = "2004-09-04"

    response = user_update(id, name, email, password, birth_date)

    return jsonify(response)


@user_bp.route('/user/delete', methods=['PATCH'])
def userDelete():
    data = request.get_json()
    id = data.get('id')

    response = user_delete(id)

    return jsonify(response)
