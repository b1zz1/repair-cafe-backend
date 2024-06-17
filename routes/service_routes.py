from flask import Blueprint, request, jsonify
from database.db import *

service_bp = Blueprint('service_bp', __name__)


@service_bp.route('/service/create', methods=['POST'])
def serviceCreate():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    description = data.get('description')
    phone = data.get('phone')

    response = service_create(name, email, description, phone)

    return jsonify(response)


@service_bp.route('/service/read', methods=['GET'])
def serviceRead():
    data = request.get_json()
    id = data.get('id')

    service = service_read(id)

    return jsonify(service)


@service_bp.route('/service/read-all', methods=['GET'])
def ServiceReadAll():
    data = service_read_all()

    return jsonify(data)


@service_bp.route('/service/update', methods=['PUT'])
def serviceUpdate():
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    email = data.get('email')
    description = data.get('description')
    phone = data.get('phone')

    response = service_update(id, name, email, description, phone)

    return jsonify(response)


@service_bp.route('/service/delete', methods=['PATCH'])
def serviceDelete():
    data = request.get_json()
    id = data.get('id')

    response = service_delete(id)

    return jsonify(response)
