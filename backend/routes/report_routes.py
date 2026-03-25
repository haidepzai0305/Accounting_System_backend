from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

report_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@report_bp.route('/income', methods=['GET'])
@jwt_required()
def get_report_income():
    return jsonify({
        "period": "Tháng 3/2024",
        "rows": [
            {"label": "DOANH THU", "isSection": True},
            {"label": "Doanh thu bán hàng", "isSubItem": True, "amount": "1,200,000,000"},
            {"label": "TỔNG CỘNG DOANH THU", "isTotal": True, "amount": "1,200,000,000"},
            {"label": "CHI PHÍ", "isSection": True},
            {"label": "Chi phí lương", "isSubItem": True, "amount": "800,000,000"},
            {"label": "TỔNG CHI PHÍ", "isTotal": True, "amount": "800,000,000"}
        ],
        "profitAmount": "400,000,000",
        "profitPeriod": "Q1"
    })

@report_bp.route('/balance', methods=['GET'])
@jwt_required()
def get_report_balance():
    return jsonify({
        "date": "2024-03-20",
        "rows": [
            {"label": "TÀI SẢN", "isSection": True},
            {"label": "Tiền mặt", "isSubItem": True, "amount": "500,000,000"},
            {"label": "Tiền gửi ngân hàng", "isSubItem": True, "amount": "1,500,000,000"},
            {"label": "TỔNG CỘNG TÀI SẢN", "isTotal": True, "amount": "2,000,000,000"}
        ],
        "isBalanced": True
    })

@report_bp.route('/chart', methods=['GET'])
@jwt_required()
def get_report_chart():
    return jsonify({
        "expenseLabels": ["Lương", "Thuê văn phòng", "Marketing", "Điện nước"],
        "expenseValues": [800, 100, 50, 20],
        "trendLabels": ["T1", "T2", "T3"],
        "trendIncome": [1100, 1150, 1200],
        "trendExpense": [750, 780, 800]
    })
