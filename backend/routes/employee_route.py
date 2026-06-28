from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from backend.services.employee_service import get_employees, create_employee

employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')


@employees_bp.route('', methods=['GET'])
@jwt_required()
def employees_list():

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    employees, total = get_employees(page, limit)

    return jsonify({
        "status": "success",
        "data": {
            "employees": [e.to_dict() for e in employees.items],
            "total": total
        }
    })

@employees_bp.route('', methods=['POST'])
@jwt_required()
def add_employee():
    try:
        data = request.get_json()
        
        # Các trường bắt buộc: employee_id, full_name, department, basic_salary, join_date
        required_fields = ['employee_id', 'full_name', 'department', 'basic_salary', 'join_date']
        
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({
                "status": "error",
                "message": f"Thiếu các trường bắt buộc: {', '.join(missing)}"
            }), 400
            
        employee = create_employee(data)
        
        return jsonify({
            "status": "success",
            "message": "Thêm nhân viên thành công!",
            "data": employee.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500