from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

home_bp = Blueprint('home', __name__, url_prefix='/api/home')

@home_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    # Mock data matching frontend HomeStat interface
    data = [
        {
            "label": "Tổng doanh thu",
            "value": "1,250,000,000đ",
            "change": "+12.5%",
            "changeType": "up",
            "icon": "TrendingUp",
            "color": "#10b981",
            "bg": "#ecfdf5"
        },
        {
            "label": "Tổng chi phí",
            "value": "840,000,000đ",
            "change": "+8.2%",
            "changeType": "down",
            "icon": "TrendingDown",
            "color": "#ef4444",
            "bg": "#fef2f2"
        },
        {
            "label": "Lợi nhuận ròng",
            "value": "410,000,000đ",
            "change": "+15.3%",
            "changeType": "up",
            "icon": "DollarSign",
            "color": "#6366f1",
            "bg": "#eef2ff"
        },
        {
            "label": "Số dư hiện tại",
            "value": "2,100,500,000đ",
            "change": "+2.4%",
            "changeType": "up",
            "icon": "Wallet",
            "color": "#f59e0b",
            "bg": "#fffbeb"
        }
    ]
    return jsonify(data)

@home_bp.route('/chart', methods=['GET'])
@jwt_required()
def get_chart():
    # Mock data matching frontend HomeChartData interface
    data = {
        "labels": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"],
        "income": [120, 150, 180, 140, 200, 220, 190, 210, 250, 230, 280, 300],
        "expense": [80, 90, 110, 100, 130, 140, 120, 130, 160, 150, 180, 190]
    }
    return jsonify(data)

@home_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    # Mock data matching frontend HomeTransaction interface
    data = [
        {
            "date": "2024-03-20",
            "category": "Bán hàng",
            "amount": "15,000,000",
            "status": "Hoàn thành",
            "type": "income"
        },
        {
            "date": "2024-03-19",
            "category": "Tiền thuê văn phòng",
            "amount": "25,000,000",
            "status": "Hoàn thành",
            "type": "expense"
        },
        {
            "date": "2024-03-18",
            "category": "Dịch vụ phần mềm",
            "amount": "5,500,000",
            "status": "Đang xử lý",
            "type": "expense"
        }
    ]
    return jsonify(data)
