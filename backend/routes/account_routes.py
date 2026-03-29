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

@account_bp.route('/bank/details', methods=['GET'])
@jwt_required()
def get_bank_details():
    return jsonify({
        "accounts": [
            {
                "id": "1", "name": "Chase Manhattan Business", "bankName": "JPMorgan Chase",
                "accountNumber": "****4821", "type": "checking", "balance": 1240500.00, "balanceChange": 2.4,
                "lastReconciled": "Oct 24, 2023", "daysSince": 12, "status": "active",
                "apiConnection": "Chase Banking API v2.4", "icon": "🏦", "color": "#2563eb"
            },
            {
                "id": "2", "name": "Wells Fargo Business Savings", "bankName": "Wells Fargo",
                "accountNumber": "****3390", "type": "savings", "balance": 875200.50, "balanceChange": 1.8,
                "lastReconciled": "Oct 20, 2023", "daysSince": 16, "status": "active",
                "apiConnection": "Wells Fargo API v1.9", "icon": "🏛️", "color": "#10b981"
            },
            {
                "id": "3", "name": "Citi Corporate Credit Line", "bankName": "Citibank",
                "accountNumber": "****7714", "type": "credit", "balance": -45000.00, "balanceChange": -0.5,
                "lastReconciled": "Oct 18, 2023", "daysSince": 18, "status": "active",
                "apiConnection": "Citi API v3.1", "icon": "💳", "color": "#f97316"
            },
            {
                "id": "4", "name": "Morgan Stanley Investment", "bankName": "Morgan Stanley",
                "accountNumber": "****9902", "type": "investment", "balance": 2180000.00, "balanceChange": 5.2,
                "lastReconciled": "Oct 15, 2023", "daysSince": 21, "status": "inactive",
                "apiConnection": "Not connected", "icon": "📈", "color": "#8b5cf6"
            }
        ],
        "transactions": {
            "1": [
                { "date": "Nov 05, 2023", "description": "Apple Store – Corporate Order", "subDesc": "Equipment Purchase", "category": "equipment", "refId": "TXN-992-084", "amount": -12450.00, "balance": 1240500.00, "icon": "🍎" },
                { "date": "Nov 04, 2023", "description": "AWS Cloud Services Payment", "subDesc": "Monthly Infrastructure", "category": "software", "refId": "TXN-118-932", "amount": -4200.50, "balance": 1252950.00, "icon": "☁️" },
                { "date": "Nov 02, 2023", "description": "Monthly Retainer – Client A", "subDesc": "Professional Services", "category": "income", "refId": "TXN-442-110", "amount": 45000.00, "balance": 1257150.50, "icon": "💼" },
                { "date": "Oct 31, 2023", "description": "Office Lease Payment", "subDesc": "HQ Rent – Month 10", "category": "rent", "refId": "TXN-301-884", "amount": -15000.00, "balance": 1212150.50, "icon": "🏢" },
                { "date": "Oct 29, 2023", "description": "Tax Consulting Fee", "subDesc": "Q3 Advisory Services", "category": "consulting", "refId": "TXN-881-289", "amount": -2500.00, "balance": 1227150.50, "icon": "📋" }
            ]
        }
    })

@account_bp.route('/chart', methods=['GET'])
@jwt_required()
def get_chart_of_accounts():
    return jsonify({
        "accounts": [
            {
                "code": '1000', "name": 'Assets', "description": 'Resources owned by the entity',
                "type": 'GROUP', "balance": 4282900.50, "status": 'active', "isGroup": True, "category": 'assets',
                "children": [
                    { "code": '1010', "name": 'Operating Cash', "description": 'Main business checking account', "type": 'Liquid Assets', "balance": 142850.42, "status": 'active', "category": 'assets' },
                    { "code": '1200', "name": 'Accounts Receivable', "description": 'Outstanding customer invoices', "type": 'Current Asset', "balance": 450200.00, "status": 'active', "category": 'assets' },
                    { "code": '1500', "name": 'Fixed Assets', "description": 'Long-term tangible property', "type": 'Non-Current Asset', "balance": 3689850.08, "status": 'active', "category": 'assets' },
                ],
            },
            {
                "code": '2000', "name": 'Liabilities', "description": 'Obligations to external parties',
                "type": 'GROUP', "balance": 1104220.00, "status": 'active', "isGroup": True, "category": 'liabilities',
                "children": [
                    { "code": '2100', "name": 'Accounts Payable', "description": 'Outstanding vendor invoices', "type": 'Current Liability', "balance": 254220.00, "status": 'active', "category": 'liabilities' },
                    { "code": '2500', "name": 'Long-Term Debt', "description": 'Bank loans and bonds payable', "type": 'Non-Current Liability', "balance": 850000.00, "status": 'active', "category": 'liabilities' },
                ],
            },
            {
                "code": '3000', "name": 'Equity', "description": "Owner's stake in the company",
                "type": 'GROUP', "balance": 3178680.50, "status": 'active', "isGroup": True, "category": 'equity',
                "children": [
                    { "code": '3100', "name": 'Common Stock', "description": 'Issued share capital', "type": 'Equity', "balance": 1000000.00, "status": 'active', "category": 'equity' },
                    { "code": '3200', "name": 'Retained Earnings', "description": 'Cumulative undistributed profit', "type": 'Equity', "balance": 2178680.50, "status": 'active', "category": 'equity' },
                ],
            },
            {
                "code": '4000', "name": 'Revenue', "description": 'Income from business activities',
                "type": 'GROUP', "balance": 2450000.00, "status": 'active', "isGroup": True, "category": 'revenue',
                "children": [
                    { "code": '4100', "name": 'Product Sales', "description": 'Revenue from core inventory sales', "type": 'Operating Income', "balance": 1890000.00, "status": 'active', "category": 'revenue' },
                    { "code": '4200', "name": 'Consulting Fees', "description": 'Deprecated - Use Service Revenue instead', "type": 'Service Income', "balance": 0.00, "status": 'inactive', "category": 'revenue' },
                    { "code": '4300', "name": 'Service Revenue', "description": 'Professional services rendered', "type": 'Service Income', "balance": 560000.00, "status": 'active', "category": 'revenue' },
                ],
            },
            {
                "code": '5000', "name": 'Expenses', "description": 'Costs incurred in operations',
                "type": 'GROUP', "balance": 1608000.00, "status": 'active', "isGroup": True, "category": 'expense',
                "children": [
                    { "code": '5100', "name": 'Payroll Expense', "description": 'Employee salaries and wages', "type": 'Operating Expense', "balance": 982400.00, "status": 'active', "category": 'expense' },
                    { "code": '5200', "name": 'Rent & Utilities', "description": 'Office space and energy costs', "type": 'Operating Expense', "balance": 312000.00, "status": 'active', "category": 'expense' },
                    { "code": '5300', "name": 'Marketing', "description": 'Advertising and promotion', "type": 'Operating Expense', "balance": 313600.00, "status": 'active', "category": 'expense' },
                ],
            },
        ],
        "transactions": {
            '1010': [
                { "date": 'Oct 28, 2023', "description": 'Global Cloud Services – Subscription', "subDesc": 'Monthly infrastructure renewal', "refId": 'INV-88921', "debit": None, "credit": 1250.00, "balance": 142850.42 },
                { "date": 'Oct 26, 2023', "description": 'Client Deposit – Horizon Corp', "subDesc": 'Project Milestone B-2', "refId": 'DEP-00421', "debit": 15000.00, "credit": None, "balance": 144100.42 },
                { "date": 'Oct 24, 2023', "description": 'Payroll – Bi-Weekly Cycle', "subDesc": 'Executive & Administrative Staff', "refId": 'PAY-10029', "debit": None, "credit": 42300.00, "balance": 129100.42 },
                { "date": 'Oct 21, 2023', "description": 'Office Lease – Metropol Tower', "subDesc": 'HQ Rent Payment (Month 10)', "refId": 'TXN-77210', "debit": None, "credit": 8500.00, "balance": 171400.42 },
                { "date": 'Oct 19, 2023', "description": 'Wire Transfer Inbound', "subDesc": 'Stellar Partners Equity Div.', "refId": 'WIR-44021', "debit": 22450.00, "credit": None, "balance": 179900.42 },
            ],
        }
    })
