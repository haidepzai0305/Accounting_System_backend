from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

payroll_bp = Blueprint('payroll', __name__, url_prefix='/api/payroll')

@payroll_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_payroll_stats():
    return jsonify({
        "employeeCount": 25,
        "totalGross": "850,000,000",
        "totalNet": "780,000,000",
        "isCalculated": True
    })

@payroll_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_payroll_employees():
    return jsonify([
        {
            "id": "EMP001",
            "name": "Nguyễn Văn A",
            "code": "NV001",
            "department": "IT",
            "bhxh": "2,400,000",
            "bhyt": "450,000",
            "netSalary": "25,000,000",
            "status": "Phê duyệt"
        },
        {
            "id": "EMP002",
            "name": "Trần Thị B",
            "code": "NV002",
            "department": "Kế toán",
            "bhxh": "1,800,000",
            "bhyt": "337,500",
            "netSalary": "18,000,000",
            "status": "Đã thanh toán"
        }
    ])

@payroll_bp.route('/calculate', methods=['POST'])
@jwt_required()
def calculate_payroll():
    data = request.get_json()
    month = data.get('month')
    return jsonify({
        "message": f"Đã tính lương cho tháng {month}",
        "count": 25
    })


@payroll_bp.route('/employees/<employee_id>/detail', methods=['GET'])
@jwt_required()
def get_payroll_detail(employee_id):
    # Mock payroll detail data matching frontend PayrollDetail interface
    detail_map = {
        "EMP001": {
            "baseSalary": 30000000,
            "allowance": 5000000,
            "grossSalary": 35000000,
            "bhxh": 2400000,
            "bhyt": 450000,
            "incomeTax": 7150000,
            "totalDeduction": 10000000,
            "netSalary": 25000000
        },
        "EMP002": {
            "baseSalary": 22500000,
            "allowance": 3500000,
            "grossSalary": 26000000,
            "bhxh": 1800000,
            "bhyt": 337500,
            "incomeTax": 5862500,
            "totalDeduction": 8000000,
            "netSalary": 18000000
        }
    }
    # Default mock data if employee_id not in map
    detail = detail_map.get(employee_id, {
        "baseSalary": 12000000,
        "allowance": 2000000,
        "grossSalary": 14000000,
        "bhxh": 960000,
        "bhyt": 180000,
        "incomeTax": 200000,
        "totalDeduction": 1340000,
        "netSalary": 12660000
    })
    return jsonify(detail)


@payroll_bp.route('/employees/<employee_id>', methods=['PUT'])
@jwt_required()
def update_payroll_status(employee_id):
    data = request.get_json()
    status = data.get('status')
    note = data.get('note', '')
    return jsonify({
        "message": f"Đã cập nhật trạng thái nhân viên {employee_id} thành '{status}'"
    })

