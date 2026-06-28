from flask import Blueprint, jsonify
from backend.models import JournalEntry, ChartOfAccounts

journal_bp = Blueprint("journal", __name__, url_prefix="/api/journal")

@journal_bp.route("", methods=["GET"])
def get_journal_entries():
    try:
        entries = JournalEntry.query.order_by(JournalEntry.date.desc(), JournalEntry.created_at.desc()).all()
        result = []
        for entry in entries:
            # Need to get account names, assuming the simplest approach here
            debit_acc = ChartOfAccounts.query.filter_by(code=entry.account_debit).first()
            credit_acc = ChartOfAccounts.query.filter_by(code=entry.account_credit).first()
            
            result.append({
                "id": entry.journal_id,
                "transId": entry.transaction_id or "N/A",
                "description": entry.description,
                "status": "Posted" if entry.status == "posted" else ("Draft" if entry.status == "draft" else "Pending Approval"),
                "systemGenerated": entry.is_system_generated,
                "accountingPeriod": entry.period or entry.date.strftime("%Y-%m"),
                "postDate": entry.date.isoformat(),
                "enteredBy": "System" if entry.is_system_generated else "User",
                "debitAccountCode": entry.account_debit,
                "debitAccountName": debit_acc.name if debit_acc else "Unknown Account",
                "debitAmount": entry.amount,
                "debitUpdatedBal": debit_acc.balance if debit_acc else 0,
                "creditAccountCode": entry.account_credit,
                "creditAccountName": credit_acc.name if credit_acc else "Unknown Account",
                "creditAmount": entry.amount,
                "creditUpdatedBal": credit_acc.balance if credit_acc else 0,
            })
            
        return jsonify({"status": "success", "data": result}), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500
