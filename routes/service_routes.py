from flask import Blueprint, request, jsonify
from database.db import *

service_bp = Blueprint('service_bp', __name__)


@service_bp.route('/service/create', methods=['POST'])
def service_create():
    data = request.get_json()
    name = data['name']
    email = data['email']
    description = data['description']
    phone = data['phone']

    response = service_create_db(name, email, description, phone)

    return jsonify(response)


@service_bp.route('/service/read', methods=['GET'])
def service_read():
    services = service_read_db()

    return jsonify(services)


@service_bp.route('/service/update', methods=['PUT'])
def service_update():
    data = request.get_json()
    service_id = data['id']
    name = data.get('name')
    email = data.get('email')
    description = data.get('description')
    phone = data.get('phone')

    response = service_update_db(service_id, name, email, description, phone)

    return jsonify(response)


@service_bp.route('/service/delete', methods=['DELETE'])
def service_delete():
    pass
