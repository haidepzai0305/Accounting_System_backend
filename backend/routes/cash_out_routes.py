from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from backend.enums.TransactionStatus import TransactionStatusEnum
from backend.models import ChartOfAccounts, CashOutDetail , db
from backend.services.audit_service import create_audit_log
from backend.services.journal_service import create_journal_entry
from backend.utils.id_generator import generate_id

cash_out_bp = Blueprint(
    "cash_out",
    __name__,
    url_prefix="/api/cash-out"
)


# =============================
# CREATE CASH OUT
# =============================
@cash_out_bp.route("", methods=["POST"])
@jwt_required()
def create_cash_out():

    try:

        user_id = get_jwt_identity()
        data = request.get_json()

        required = ["date", "amount", "description", "account_debit", "account_credit", "category"]

        if not all(field in data for field in required):
            missing = [f for f in required if f not in data]
            return jsonify({
                "status": "error",
                "message": f"Thiếu các trường bắt buộc: {', '.join(missing)}"
            }), 400

        # validate accounts
        debit_account = ChartOfAccounts.query.filter_by(
            code=data["account_debit"]
        ).first()

        credit_account = ChartOfAccounts.query.filter_by(
            code=data["account_credit"]
        ).first()

        if not debit_account or not credit_account:
            return jsonify({
                "status": "error",
                "message": "Account not found"
            }), 400

        transaction = CashOutDetail(

            transaction_id=generate_id("TRX"),

            date=datetime.strptime(
                data["date"],
                "%Y-%m-%d"
            ).date(),

            amount=data["amount"],

            currency=data.get("currency", "VND"),

            category=data.get("category"),

            description=data["description"],

            account_debit=data["account_debit"],

            account_credit=data["account_credit"],

            bank_account_id=data.get("bank_account_id"),

            status=TransactionStatusEnum.PENDING,

            notes=data.get("notes"),

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

        create_audit_log(
            user_id,
            "create",
            "cash_out_details",
            transaction.id,
            None,
            transaction.to_dict()
        )

        db.session.commit()

        return jsonify({
            "status": "success",
            "data": {
                "id": transaction.id,
                "transaction_id": transaction.transaction_id,
                "journal_id": journal.journal_id
            }
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# =============================
# LIST CASH OUT
# =============================
@cash_out_bp.route("", methods=["GET"])
@jwt_required()
def get_cash_out_list():

    try:

        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 20, type=int)
        status = request.args.get("status")

        query = CashOutDetail.query

        if status:
            query = query.filter_by(
                status=TransactionStatusEnum[status.upper()]
            )

        query = query.order_by(
            CashOutDetail.created_at.desc()
        )

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



@cash_out_bp.route("/<int:transaction_id>", methods=["GET"])
@jwt_required()
def get_cash_out_detail(transaction_id):

    transaction = CashOutDetail.query.get(transaction_id)

    if not transaction:

        return jsonify({
            "status": "error",
            "message": "Transaction not found"
        }), 404

    return jsonify({

        "status": "success",

        "data": transaction.to_dict()
    })



@cash_out_bp.route("/<int:transaction_id>/approve", methods=["PATCH"])
@jwt_required()
def approve_cash_out(transaction_id):

    try:

        user_id = get_jwt_identity()

        transaction = CashOutDetail.query.get(transaction_id)

        if not transaction:

            return jsonify({
                "status": "error",
                "message": "Transaction not found"
            }), 404

        old_data = transaction.to_dict()

        transaction.status = TransactionStatusEnum.APPROVED

        transaction.approved_by = user_id

        transaction.approved_at = datetime.utcnow()

        db.session.commit()

        create_audit_log(
            user_id,
            "approve",
            "cash_out_details",
            transaction.id,
            old_data,
            transaction.to_dict()
        )

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Transaction approved"
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



@cash_out_bp.route("/<int:transaction_id>/reject", methods=["PATCH"])
@jwt_required()
def reject_cash_out(transaction_id):

    try:

        user_id = get_jwt_identity()

        data = request.get_json()

        transaction = CashOutDetail.query.get(transaction_id)

        if not transaction:

            return jsonify({
                "status": "error",
                "message": "Transaction not found"
            }), 404

        old_data = transaction.to_dict()

        transaction.status = TransactionStatusEnum.REJECTED

        transaction.rejection_reason = data.get("reason")

        db.session.commit()

        create_audit_log(
            user_id,
            "reject",
            "cash_out_details",
            transaction.id,
            old_data,
            transaction.to_dict()
        )

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Transaction rejected"
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500