from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.services import payroll_service

payroll_bp = Blueprint('payroll', __name__, url_prefix='/api/payroll')


@payroll_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_payroll_stats():
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    stats = payroll_service.get_payroll_stats(month=month, year=year)
    return jsonify(stats)


@payroll_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_payroll_employees():
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    employees, total = payroll_service.get_payroll_employees(
        month=month, year=year, page=page, limit=limit
    )
    return jsonify(employees)


@payroll_bp.route('/calculate', methods=['POST'])
@jwt_required()
def calculate_payroll():
    data = request.get_json()
    month = data.get('month')
    year = data.get('year')
    user_id = get_jwt_identity()

    if not month or not year:
        return jsonify({"error": "Vui lòng cung cấp tháng và năm"}), 400

    result = payroll_service.calculate_payroll_for_month(month, year, created_by=user_id)
    return jsonify(result)


@payroll_bp.route('/', methods=['POST'])
@jwt_required()
def create_payroll():
    data = request.get_json()
    user_id = get_jwt_identity()

    required_fields = ['employee_id', 'month', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Thiếu trường bắt buộc: {field}"}), 400

    try:
        payroll = payroll_service.create_payroll(data, created_by=user_id)
        return jsonify(payroll.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@payroll_bp.route('/employees/<employee_id>/detail', methods=['GET'])
@jwt_required()
def get_payroll_detail(employee_id):
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    # Thử tìm theo payroll_id trước, nếu không thì tìm theo employee_id
    detail = payroll_service.get_payroll_detail(employee_id)

    if not detail:
        # Tìm theo employee primary key hoặc employee_id string
        from backend.models.Employee import Employee
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        if employee:
            detail = payroll_service.get_payroll_by_employee(
                employee.id, month=month, year=year
            )

    if not detail:
        return jsonify({
            "baseSalary": 0,
            "allowance": 0,
            "grossSalary": 0,
            "bhxh": 0,
            "bhyt": 0,
            "incomeTax": 0,
            "totalDeduction": 0,
            "netSalary": 0
        })

    return jsonify(detail)


@payroll_bp.route('/employees/<employee_id>', methods=['PUT'])
@jwt_required()
def update_payroll_status(employee_id):
    data = request.get_json()
    status = data.get('status')
    note = data.get('note', '')
    user_id = get_jwt_identity()

    if not status:
        return jsonify({"error": "Vui lòng cung cấp trạng thái"}), 400

    try:
        payroll = payroll_service.update_payroll_status(
            payroll_id=employee_id,
            status=status,
            user_id=user_id,
            note=note
        )
        return jsonify({
            "message": f"Đã cập nhật trạng thái thành '{status}'",
            "payroll": payroll.to_dict()
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@payroll_bp.route('/<payroll_id>', methods=['DELETE'])
@jwt_required()
def delete_payroll(payroll_id):
    try:
        payroll_service.delete_payroll(payroll_id)
        return jsonify({"message": "Đã xóa bảng lương thành công"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
