from flask import Blueprint, send_file, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

from backend.models import CashInDetail, CashOutDetail, db
from backend.models.Employee import Employee
from backend.models.Payroll import Payroll
from backend.enums.TransactionStatus import TransactionStatusEnum
from backend.services.export_service import build_excel

export_bp = Blueprint("export", __name__, url_prefix="/api/export")


# =============================
# EXPORT CASH IN
# =============================
@export_bp.route("/cash-in", methods=["GET"])
@jwt_required()
def export_cash_in():
    try:
        status     = request.args.get("status")
        start_date = request.args.get("start_date")
        end_date   = request.args.get("end_date")

        query = CashInDetail.query

        if status:
            query = query.filter_by(status=TransactionStatusEnum[status.upper()])

        if start_date:
            query = query.filter(CashInDetail.date >= datetime.strptime(start_date, "%Y-%m-%d").date())

        if end_date:
            query = query.filter(CashInDetail.date <= datetime.strptime(end_date, "%Y-%m-%d").date())

        records = query.order_by(CashInDetail.date.desc()).all()

        headers = [
            "ID", "Mã giao dịch", "Ngày", "Số tiền (VND)",
            "Tiền tệ", "Nguồn thu", "Mô tả",
            "Tài khoản Nợ", "Tài khoản Có", "Trạng thái", "Ngày tạo"
        ]

        rows = [
            [
                r.id,
                r.transaction_id,
                r.date.strftime("%d/%m/%Y"),
                r.amount,
                r.currency,
                getattr(r, "source", ""),
                r.description,
                r.account_debit,
                r.account_credit,
                r.status.value,
                r.created_at.strftime("%d/%m/%Y %H:%M") if r.created_at else ""
            ]
            for r in records
        ]

        stream   = build_excel("Danh sách Thu tiền (Cash In)", headers, rows)
        filename = f"cash_in_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return send_file(
            stream,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============================
# EXPORT CASH OUT
# =============================
@export_bp.route("/cash-out", methods=["GET"])
@jwt_required()
def export_cash_out():
    try:
        status     = request.args.get("status")
        start_date = request.args.get("start_date")
        end_date   = request.args.get("end_date")

        query = CashOutDetail.query

        if status:
            query = query.filter_by(status=TransactionStatusEnum[status.upper()])

        if start_date:
            query = query.filter(CashOutDetail.date >= datetime.strptime(start_date, "%Y-%m-%d").date())

        if end_date:
            query = query.filter(CashOutDetail.date <= datetime.strptime(end_date, "%Y-%m-%d").date())

        records = query.order_by(CashOutDetail.date.desc()).all()

        headers = [
            "ID", "Mã giao dịch", "Ngày", "Số tiền (VND)",
            "Tiền tệ", "Danh mục", "Mô tả",
            "Tài khoản Nợ", "Tài khoản Có", "Trạng thái",
            "Lý do từ chối", "Ghi chú", "Ngày tạo"
        ]

        rows = [
            [
                r.id,
                r.transaction_id,
                r.date.strftime("%d/%m/%Y"),
                r.amount,
                r.currency,
                getattr(r, "category", ""),
                r.description,
                r.account_debit,
                r.account_credit,
                r.status.value,
                r.rejection_reason or "",
                r.notes or "",
                r.created_at.strftime("%d/%m/%Y %H:%M") if r.created_at else ""
            ]
            for r in records
        ]

        stream   = build_excel("Danh sách Chi tiền (Cash Out)", headers, rows)
        filename = f"cash_out_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return send_file(
            stream,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============================
# EXPORT EMPLOYEES
# =============================
@export_bp.route("/employees", methods=["GET"])
@jwt_required()
def export_employees():
    try:
        status  = request.args.get("status")   # active / inactive / retired
        dept    = request.args.get("department")

        query = Employee.query

        if status:
            query = query.filter_by(status=status.lower())

        if dept:
            query = query.filter(Employee.department.ilike(f"%{dept}%"))

        records = query.order_by(Employee.full_name.asc()).all()

        headers = [
            "ID", "Mã nhân viên", "Họ và tên",
            "Ngày sinh", "Giới tính", "CMND/CCCD",
            "Điện thoại", "Email", "Phòng ban",
            "Chức vụ", "Lương cơ bản (VND)",
            "Ngày vào làm", "Trạng thái"
        ]

        rows = [
            [
                r.id,
                r.employee_id,
                r.full_name,
                r.date_of_birth.strftime("%d/%m/%Y") if r.date_of_birth else "",
                r.gender or "",
                r.identification_number or "",
                r.phone or "",
                r.email or "",
                r.department,
                r.position or "",
                r.basic_salary,
                r.join_date.strftime("%d/%m/%Y") if r.join_date else "",
                r.status
            ]
            for r in records
        ]

        stream   = build_excel("Danh sách Nhân viên", headers, rows)
        filename = f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return send_file(
            stream,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============================
# EXPORT PAYROLL
# =============================
@export_bp.route("/payroll", methods=["GET"])
@jwt_required()
def export_payroll():
    try:
        month  = request.args.get("month", type=int)
        year   = request.args.get("year", type=int)
        status = request.args.get("status")

        query = db.session.query(Payroll, Employee).join(
            Employee, Payroll.employee_id == Employee.id
        )

        if month:
            query = query.filter(Payroll.month == month)

        if year:
            query = query.filter(Payroll.year == year)

        if status:
            from backend.enums.PayrollStatus import PayrollStatusEnum
            query = query.filter(Payroll.status == PayrollStatusEnum[status.upper()])

        records = query.order_by(Payroll.year.desc(), Payroll.month.desc()).all()

        headers = [
            "ID", "Mã bảng lương", "Tháng", "Năm",
            "Mã NV", "Tên nhân viên", "Phòng ban",
            "Lương cơ bản", "Phụ cấp", "Tổng lương gộp",
            "BHXH (8%)", "BHYT (1.5%)", "Thuế TNCN",
            "Tổng khấu trừ", "Lương thực nhận",
            "Trạng thái", "Ghi chú"
        ]

        rows = [
            [
                p.id,
                p.payroll_id,
                p.month,
                p.year,
                e.employee_id,
                e.full_name,
                e.department,
                p.basic_salary,
                p.allowance,
                p.brutto_salary,
                p.bhxh_amount,
                p.bhyt_amount,
                p.tax_amount,
                p.total_deductions,
                p.netto_salary,
                p.status.value,
                p.notes or ""
            ]
            for p, e in records
        ]

        period   = f"T{month:02d}-{year}" if month and year else "all"
        stream   = build_excel(f"Bảng lương {period}", headers, rows)
        filename = f"payroll_{period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return send_file(
            stream,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
