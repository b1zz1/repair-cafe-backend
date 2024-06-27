from flask import Blueprint, request, jsonify
from database.db import *

service_bp = Blueprint('service_bp', __name__)


@service_bp.route('/service/create', methods=['POST'])
def serviceCreate():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    description = data.get('description')
    phone = data.get('whatsapp')

    response = service_create(name, email, description, phone)

    return jsonify(response)


@service_bp.route('/service/read/<int:id>', methods=['GET'])
def serviceRead(id):
    service = service_read(id)

    return jsonify(service)


# @service_bp.route('/service/read-by-expertise', methods=['GET'])
# def serviceReadByExpertise():
#     data = service_read_by_expertise()
#
#     return jsonify(data)


@service_bp.route('/service/read-all-by-expertise', methods=['GET'])
def serviceReadAllByExpertise():
    data = service_read_all_by_expertise()

    return jsonify(data)


@service_bp.route('/service/read-all', methods=['GET'])
def ServiceReadAll():
    data = service_read_all()

    return jsonify(data)


@service_bp.route('/service/update/<int:id>', methods=['PUT'])
def serviceUpdate(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    description = data.get('description')
    phone = data.get('phone')

    response = service_update(id, name, email, description, phone)

    return jsonify(response)

# @user_bp.route('/user/update/<int:id>', methods=['PUT'])
# def userUpdate(id):
#     data = request.get_json()
#     name = data.get('name')
#     surname = data.get('surname')
#     email = data.get('email')
#     birth_date = data.get('birth_date')
#     salt = generate_salt()
#     password = hash_password(data['password'], salt)
#
#     response = user_update(id, name, surname, email, password, birth_date)
#
#     return jsonify(response)

@service_bp.route('/service/delete', methods=['PATCH'])
def serviceDelete():
    data = request.get_json()
    id = data.get('id')

    response = service_delete(id)

    return jsonify(response)
