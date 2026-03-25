from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    return jsonify({
        "totalIncome": "1.2B",
        "totalExpense": "840M",
        "balance": "360M",
        "incomeChange": "+12%",
        "expenseChange": "+5%"
    })

@dashboard_bp.route('/chart', methods=['GET'])
@jwt_required()
def get_chart():
    return jsonify({
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "income": [45, 52, 38, 65, 48, 72, 58],
        "expense": [32, 41, 35, 42, 36, 45, 38],
        "expenseBreakdown": {
            "labels": ["Lương", "Văn phòng", "Marketing", "Khác"],
            "values": [40, 25, 20, 15]
        }
    })

@dashboard_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    return jsonify([
        {"date": "2024-03-20", "description": "Lương tháng 3", "amount": "500,000,000", "type": "expense", "status": "approved"},
        {"date": "2024-03-19", "description": "Hợp đồng dự án A", "amount": "250,000,000", "type": "income", "status": "approved"},
        {"date": "2024-03-18", "description": "Tiện ích văn phòng", "amount": "12,000,000", "type": "expense", "status": "pending"}
    ])

@dashboard_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    return jsonify([
        {"name": "Phê duyệt bảng lương", "count": 2, "priority": "high"},
        {"name": "Báo cáo thuế Q1", "count": 1, "priority": "high"},
        {"name": "Đối soát ngân hàng", "count": 5, "priority": "medium"}
    ])
