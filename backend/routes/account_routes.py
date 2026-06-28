from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from backend.models import ChartOfAccounts, BankAccount, JournalEntry, db
from backend.enums.AccountType import AccountTypeEnum

account_bp = Blueprint('accounts', __name__, url_prefix='/api/accounts')

@account_bp.route('', methods=['GET'])
@jwt_required()
def get_accounts():
    """Fetch all accounts from the Chart of Accounts."""
    accounts = ChartOfAccounts.query.filter_by(is_active=True).all()
    
    # If the database is empty, return initial mock structure so UI doesn't break
    if not accounts:
        return jsonify({
            "debit": [],
            "credit": []
        })

    return jsonify({
        "debit": [a.to_dict() for a in accounts if a.type in [AccountTypeEnum.ASSET, AccountTypeEnum.EXPENSE]],
        "credit": [a.to_dict() for a in accounts if a.type in [AccountTypeEnum.LIABILITY, AccountTypeEnum.EQUITY, AccountTypeEnum.REVENUE]]
    })

@account_bp.route('/bank', methods=['GET'])
@jwt_required()
def get_bank_accounts():
    """Fetch all active bank accounts."""
    banks = BankAccount.query.filter_by(status='active').all()
    return jsonify([
        {"value": str(bank.id), "label": f"{bank.bank_name} - {bank.account_number}"}
        for bank in banks
    ])

@account_bp.route('/bank/details', methods=['GET'])
@jwt_required()
def get_bank_details():
    """Fetch detailed bank account info and recent transactions."""
    banks = BankAccount.query.all()
    accounts_data = []
    
    # Predefined colors/icons for better UI
    bank_styles = {
        "Vietcombank": {"icon": "🏦", "color": "#2563eb"},
        "Techcombank": {"icon": "🏛️", "color": "#10b981"},
        "MB Bank": {"icon": "💳", "color": "#f97316"},
        "TP Bank": {"icon": "📈", "color": "#8b5cf6"}
    }

    for bank in banks:
        style = bank_styles.get(bank.bank_name, {"icon": "🏦", "color": "#6366f1"})
        accounts_data.append({
            "id": str(bank.id),
            "name": bank.account_holder,
            "bankName": bank.bank_name,
            "accountNumber": f"****{bank.account_number[-4:]}",
            "type": bank.account_type or "checking",
            "balance": float(bank.balance),
            "balanceChange": 0, # Could be calculated from transactions
            "lastReconciled": bank.last_reconciled_at.strftime("%b %d, %Y") if bank.last_reconciled_at else "Never",
            "daysSince": (datetime.utcnow() - bank.last_reconciled_at).days if bank.last_reconciled_at else 0,
            "status": bank.status,
            "apiConnection": "Active",
            "icon": style["icon"],
            "color": style["color"]
        })

    # For transactions, we can pull recent JournalEntries if they involve a bank account
    # For now, let's just use the current bank journals link if we have them
    transactions_data = {}
    for bank in banks:
        # Assuming we can find bank accounts in ChartOfAccounts by code or similar
        # For a simple mock-to-real replacement, we'll try to find recent entries
        # matching some logic, or just return empty for now if not linked
        entries = JournalEntry.query.filter(
            (JournalEntry.account_debit.like('112%')) | 
            (JournalEntry.account_credit.like('112%'))
        ).order_by(JournalEntry.date.desc()).limit(10).all()
        
        transactions_data[str(bank.id)] = [
            {
                "date": entry.date.strftime("%b %d, %Y"),
                "description": entry.description,
                "subDesc": entry.notes or "",
                "category": "General", # Could be mapped from accounts
                "refId": entry.journal_id,
                "amount": float(entry.amount) if entry.account_debit.startswith('112') else -float(entry.amount),
                "balance": 0, # Running balance would be more complex
                "icon": "💳"
            } for entry in entries
        ]

    return jsonify({
        "accounts": accounts_data,
        "transactions": transactions_data
    })

@account_bp.route('/chart', methods=['GET'])
@jwt_required()
def get_chart_of_accounts():
    """Fetch the full hierarchy of Chart of Accounts."""
    all_accounts = ChartOfAccounts.query.order_by(ChartOfAccounts.code).all()
    
    # Build a dictionary to easily find parents
    accounts_by_code = {acc.code: acc.to_dict() for acc in all_accounts}
    for code, data in accounts_by_code.items():
        data['children'] = []
        data['isGroup'] = False # Default

    roots = []
    for acc in all_accounts:
        data = accounts_by_code[acc.code]
        if acc.parent_account_code and acc.parent_account_code in accounts_by_code:
            accounts_by_code[acc.parent_account_code]['children'].append(data)
            accounts_by_code[acc.parent_account_code]['isGroup'] = True
        else:
            roots.append(data)

    # Get recent transactions for each active account (top level or as needed)
    transactions_data = {}
    # Fetch some recent journal entries to populate graphs/lists
    recent_entries = JournalEntry.query.order_by(JournalEntry.date.desc()).limit(50).all()
    
    for entry in recent_entries:
        # Group by debit account
        if entry.account_debit not in transactions_data:
            transactions_data[entry.account_debit] = []
        
        transactions_data[entry.account_debit].append({
            "date": entry.date.strftime("%b %d, %Y"),
            "description": entry.description,
            "subDesc": entry.notes or "",
            "refId": entry.journal_id,
            "debit": float(entry.amount),
            "credit": None,
            "balance": 0 # Would need to be historical
        })

        # Group by credit account
        if entry.account_credit not in transactions_data:
            transactions_data[entry.account_credit] = []
            
        transactions_data[entry.account_credit].append({
            "date": entry.date.strftime("%b %d, %Y"),
            "description": entry.description,
            "subDesc": entry.notes or "",
            "refId": entry.journal_id,
            "debit": None,
            "credit": float(entry.amount),
            "balance": 0
        })

    return jsonify({
        "accounts": roots,
        "transactions": transactions_data
    })

@account_bp.route('', methods=['POST'])
@jwt_required()
def create_account():
    try:
        data = request.get_json()
        
        # Image fields: Mã tài khoản, Tên tài khoản, Danh mục, Loại tài khoản, Diễn giải, Số dư đầu kỳ
        # Mapping to model:
        # - Mã tài khoản -> code
        # - Tên tài khoản -> name
        # - Danh mục -> type (Enum: asset, liability, etc.)
        # - Loại tài khoản -> category (String)
        # - Diễn giải -> description
        # - Số dư đầu kỳ -> balance
        
        code = data.get('code')
        name = data.get('name')
        account_type_str = data.get('type') 
        category = data.get('category')
        description = data.get('description')
        balance = data.get('balance', 0)
        parent_code = data.get('parent_account_code')
        
        if not code or not name or not account_type_str:
            return jsonify({"error": "Mã tài khoản, tên và danh mục là bắt buộc"}), 400
        
        # Check if code exists
        if ChartOfAccounts.query.filter_by(code=code).first():
            return jsonify({"error": f"Mã tài khoản '{code}' đã tồn tại"}), 400
            
        # Convert type to enum
        try:
            enum_type = AccountTypeEnum(account_type_str.lower())
        except ValueError:
            # Maybe it's sent in Vietnamese? 
            # "Tài sản" -> asset, "Nợ phải trả" -> liability, "Vốn chủ sở hữu" -> equity, "Doanh thu" -> revenue, "Chi phí" -> expense
            mapping = {
                "tài sản": AccountTypeEnum.ASSET,
                "nợ phải trả": AccountTypeEnum.LIABILITY,
                "vốn chủ sở hữu": AccountTypeEnum.EQUITY,
                "doanh thu": AccountTypeEnum.REVENUE,
                "chi phí": AccountTypeEnum.EXPENSE
            }
            enum_type = mapping.get(account_type_str.lower())
            if not enum_type:
                return jsonify({"error": f"Danh mục '{account_type_str}' không hợp lệ"}), 400
        
        new_account = ChartOfAccounts(
            code=code,
            name=name,
            type=enum_type,
            category=category,
            description=description,
            balance=balance,
            parent_account_code=parent_code
        )
        
        db.session.add(new_account)
        db.session.commit()
        
        return jsonify({
            "message": "Tạo tài khoản thành công!",
            "account": new_account.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

