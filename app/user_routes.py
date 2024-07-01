from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database.base import get_db
from crud import create_user, get_user, update_user, delete_user
from exceptions import DatabaseError
from security import generate_salt

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user/create', methods=['POST'])
def create_user_route():
    data = request.get_json()
    try:
        salt = generate_salt()
        with get_db() as db:
            user = create_user(db, data['name'], data.get('surname', ''), data['email'], data['password'], salt, data['birth_date'])
            return jsonify({'id': user.id, 'message': 'User created successfully'}), 200
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/read', methods=['GET'])
def read_user():
    user_id = request.args.get('id')
    try:
        with get_db() as db:
            user = get_user(db, user_id)
            if user:
                user_data = {
                    'name': user.name,
                    'surname': user.surname,
                    'email': user.email,
                    'password': user.password,
                    'salt': user.salt,
                    'birth_date': user.birth_date.strftime('%Y-%m-%d')
                }
                return jsonify(user_data), 200
            else:
                return jsonify({"error": f"User with ID {user_id} not found"}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/update', methods=['PUT'])
def update_user_route():
    data = request.get_json()
    try:
        with get_db() as db:
            user = update_user(db, data['id'], data.get('name'), data.get('surname'), data.get('email'), data.get('password'), data.get('birth_date'))
            if user:
                return jsonify({'id': user.id, 'message': 'User updated successfully'}), 200
            else:
                return jsonify({"error": f"User with ID {data['id']} not found"}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/delete', methods=['DELETE'])
def delete_user_route():
    data = request.get_json()
    try:
        with get_db() as db:
            user = delete_user(db, data['id'])
            if user:
                return jsonify({'id': user.id, 'message': 'User deleted successfully'}), 200
            else:
                return jsonify({"error": f"User with ID {data['id']} not found"}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500
