from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

account_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')

@account_bp.route('', methods=['GET'])
@jwt_required()
def get_accounts():
    # Mock accounts (Chart of Accounts)
    return jsonify({
        "debit": [
            {"code": "1111", "name": "Tiền mặt VND", "balance": 500000000},
            {"code": "1121", "name": "Tiền gửi ngân hàng VND", "balance": 1500000000}
        ],
        "credit": [
            {"code": "5111", "name": "Doanh thu bán hàng hóa", "balance": 0},
            {"code": "6421", "name": "Chi phí tiền lương", "balance": 0}
        ]
    })

@account_bp.route('/bank', methods=['GET'])
@jwt_required()
def get_bank_accounts():
    return jsonify([
        {"value": "vcb", "label": "Vietcombank - 0011001234567"},
        {"value": "tcb", "label": "Techcombank - 1903456789012"}
    ])
