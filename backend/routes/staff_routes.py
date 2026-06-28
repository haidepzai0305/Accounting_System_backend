from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from backend.services.employee_service import get_employees, get_employee, create_employee, update_employee
from backend.models.Employee import Employee
from backend.models import db

staff_bp = Blueprint('staff', __name__, url_prefix='/api/staff')

@staff_bp.route('', methods=['GET'])
@jwt_required()
def staff_list():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    employees, total = get_employees(page, limit)

    return jsonify([e.to_dict() for e in employees.items])

@staff_bp.route('/<int:staff_id>', methods=['GET'])
@jwt_required()
def get_staff_detail(staff_id):
    employee = get_employee(staff_id)
    if not employee:
        return jsonify({"error": "Staff not found"}), 404
    return jsonify(employee.to_dict())

@staff_bp.route('', methods=['POST'])
@jwt_required()
def add_staff():
    data = request.get_json()
    try:
        new_employee = create_employee(data)
        return jsonify(new_employee.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@staff_bp.route('/<int:staff_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_staff(staff_id):
    data = request.get_json()
    employee = get_employee(staff_id)
    if not employee:
        return jsonify({"error": "Staff not found"}), 404
    try:
        updated_employee = update_employee(employee, data)
        return jsonify(updated_employee.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@staff_bp.route('/<int:staff_id>', methods=['DELETE'])
@jwt_required()
def delete_staff(staff_id):
    employee = get_employee(staff_id)
    if not employee:
        return jsonify({"error": "Staff not found"}), 404
    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Staff deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@staff_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_staff_stats():
    # Provide simple statistics
    total_employees = Employee.query.count()
    active_employees = Employee.query.filter_by(status='active').count()
    
    return jsonify({
        "totalStaff": total_employees,
        "activeStaff": active_employees,
        "totalEmployees": total_employees,
        "activeEmployees": active_employees,
        "newHires": 0,
        "turnoverRate": 0
    })
