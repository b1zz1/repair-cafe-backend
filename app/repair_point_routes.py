from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database.base import get_db
from crud import create_repair_point, get_repair_point, get_all_repair_points, update_repair_point, delete_repair_point
from exceptions import DatabaseError

repair_point_bp = Blueprint('repair_point_bp', __name__)

@repair_point_bp.route('/repair/create', methods=['POST'])
def create_repair_point_route():
    data = request.get_json()
    try:
        with get_db() as db:
            repair_point = create_repair_point(db, data['name'], data['email'], data['description'], data['phone'], data['user_id'])
            return jsonify({'id': repair_point.id, 'message': 'Repair point created successfully'}), 200
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@repair_point_bp.route('/repair/read', methods=['GET'])
def read_repair_point():
    repair_point_id = request.args.get('id')
    try:
        with get_db() as db:
            repair_point = get_repair_point(db, repair_point_id)
            if repair_point:
                repair_point_data = {
                    'name': repair_point.name,
                    'email': repair_point.email,
                    'description': repair_point.description,
                    'phone': repair_point.phone,
                    'user_id': repair_point.user_id
                }
                return jsonify(repair_point_data), 200
            else:
                return jsonify({"error": f"Repair point with ID {repair_point_id} not found"}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@repair_point_bp.route('/repair/list', methods=['GET'])
def list_repair_points():
    try:
        with get_db() as db:
            repair_points = get_all_repair_points(db)
            repair_points_data = [{'id': rp.id, 'name': rp.name, 'email': rp.email, 'description': rp.description, 'phone': rp.phone} for rp in repair_points]
            return jsonify(repair_points_data), 200
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@repair_point_bp.route('/repair/update', methods=['PUT'])
def update_repair_point_route():
    data = request.get_json()
    try:
        with get_db() as db:
            repair_point = update_repair_point(db, data['id'], data.get('name'), data.get('email'), data.get('description'), data.get('phone'))
            if repair_point:
                return jsonify({'id': repair_point.id, 'message': 'Repair point updated successfully'}), 200
            else:
                return jsonify({"error": f"Repair point with ID {data['id']} not found"}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@repair_point_bp.route('/repair/delete', methods=['DELETE'])
def delete_repair_point_route():
    data = request.get_json()
    try:
        with get_db() as db:
            repair_point = delete_repair_point(db, data['id'])
            if repair_point:
                return jsonify({'id': repair_point.id, 'message': 'Repair point deleted successfully'}), 200
            else:
                return jsonify({"error": f"Repair point with ID {data['id']} not found"}), 404
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500
