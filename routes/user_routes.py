from flask import Blueprint, request
from database.db import *
from utils.security import hash_password, generate_salt

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user/create', methods=['POST'])
def userCreate():
    data = request.get_json()
    name = data['name']
    email = data['email']
    salt = generate_salt()
    password = hash_password(data['password'], salt)

    response = user_create(name, email, password, salt, "2005-01-01")

    return jsonify(response)


@user_bp.route('/user/read', methods=['GET'])
def userRead():
    user = user_read()

    return jsonify(user)


@user_bp.route('/user/update', methods=['GET', 'PUT'])
def userUpdate():
    pass


@user_bp.route('/user/delete', methods=['GET'])
def userDelete():
    pass
