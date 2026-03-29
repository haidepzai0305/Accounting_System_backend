from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from backend.enums.TransactionStatus import TransactionStatusEnum
from backend.models import CashInDetail, db
from backend.services.audit_service import create_audit_log
from backend.services.journal_service import create_journal_entry
from backend.utils.id_generator import generate_id

cash_in_bp = Blueprint("cash_in", __name__, url_prefix="/api/cash-in")


@cash_in_bp.route("", methods=["POST"])
@jwt_required()
def create_cash_in():

    user_id = get_jwt_identity()
    data = request.get_json()

    transaction = CashInDetail(
        transaction_id=generate_id("TRX"),
        date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
        amount=data["amount"],
        currency=data.get("currency", "VND"),
        source=data.get("source", "Khác"),  # Fixed: read source from request (NOT NULL in DB)
        description=data["description"],
        account_debit=data["account_debit"],
        account_credit=data["account_credit"],
        status=TransactionStatusEnum.PENDING,
        created_by=user_id
    )

    db.session.add(transaction)
    db.session.flush()

    journal = create_journal_entry(
        transaction.transaction_id,
        transaction.date,
        transaction.description,
        transaction.account_debit,
        transaction.account_credit,
        transaction.amount
    )

    db.session.commit()

    create_audit_log(user_id, "create", "cash_in_detail", transaction.id)
    db.session.commit()

    return jsonify({
        "status": "success",
        "journal_id": journal.journal_id
    })


# =============================
# LIST CASH IN
# =============================
@cash_in_bp.route("", methods=["GET"])
@jwt_required()
def get_cash_in_list():
    try:
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 20, type=int)
        status = request.args.get("status")

        query = CashInDetail.query

        if status:
            query = query.filter_by(
                status=TransactionStatusEnum[status.upper()]
            )

        query = query.order_by(CashInDetail.created_at.desc())

        pagination = query.paginate(
            page=page,
            per_page=limit
        )

        return jsonify({
            "status": "success",
            "data": {
                "transactions": [
                    t.to_dict() for t in pagination.items
                ],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": pagination.total,
                    "pages": pagination.pages
                }
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500