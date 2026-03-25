from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from backend.services.employee_service import get_employees

employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')


@employees_bp.route('/', methods=['GET'])
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