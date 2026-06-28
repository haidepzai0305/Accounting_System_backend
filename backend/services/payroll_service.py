from datetime import datetime

from backend.extension import db
from backend.models.Payroll import Payroll
from backend.models.Employee import Employee
from backend.enums.PayrollStatus import PayrollStatusEnum
from backend.utils.id_generator import generate_id


def get_payroll_stats(month=None, year=None):
    """Lấy thống kê tổng quan về bảng lương."""
    query = Payroll.query

    if month:
        query = query.filter_by(month=month)
    if year:
        query = query.filter_by(year=year)

    payrolls = query.all()

    employee_count = len(payrolls)
    total_gross = sum(p.brutto_salary for p in payrolls)
    total_net = sum(p.netto_salary for p in payrolls)
    is_calculated = employee_count > 0

    return {
        "employeeCount": employee_count,
        "totalGross": f"{total_gross:,}",
        "totalNet": f"{total_net:,}",
        "isCalculated": is_calculated
    }


def get_payroll_employees(month=None, year=None, page=1, limit=20):
    """Lấy danh sách TOÀN BỘ nhân viên active và thông tin lương tháng (nếu có)."""
    # 1. Lấy danh sách nhân viên đang hoạt động làm gốc
    query = Employee.query.filter_by(status='active')
    
    total = query.count()
    employees = query.order_by(Employee.employee_id.asc()) \
        .offset((page - 1) * limit).limit(limit).all()

    result = []
    for emp in employees:
        # 2. Tìm bản ghi lương cho tháng/năm này
        p = Payroll.query.filter_by(
            employee_id=emp.id, 
            month=month, 
            year=year
        ).first()
        
        # Mapping trạng thái sang tiếng Việt cho UI
        status_map = {
            PayrollStatusEnum.DRAFT: "Chờ duyệt",
            PayrollStatusEnum.CALCULATED: "Đã tính",
            PayrollStatusEnum.APPROVED: "Phê duyệt",
            PayrollStatusEnum.PAID: "Đã thanh toán"
        }

        if p:
            result.append({
                "id": p.payroll_id,
                "name": emp.full_name,
                "code": emp.employee_id,
                "department": emp.department,
                "basicSalary": f"{p.basic_salary:,}",
                "allowance": f"{p.allowance:,}",
                "bhxh": f"{p.bhxh_amount:,}",
                "bhyt": f"{p.bhyt_amount:,}",
                "netSalary": f"{p.netto_salary:,}",
                "status": status_map.get(p.status, p.status.value)
            })
        else:
            # Nếu chưa có bản ghi lương cho tháng này
            result.append({
                "id": f"NEW-{emp.employee_id}", 
                "name": emp.full_name,
                "code": emp.employee_id,
                "department": emp.department,
                "basicSalary": f"{emp.basic_salary:,}",
                "allowance": "0",
                "bhxh": "0",
                "bhyt": "0",
                "netSalary": "0",
                "status": "Chưa tính"
            })

    return result, total


def get_payroll_detail(payroll_id):
    """Lấy chi tiết bảng lương của một nhân viên."""
    payroll = Payroll.query.filter_by(payroll_id=payroll_id).first()

    if not payroll:
        return None

    return {
        "id": payroll.payroll_id,
        "employee_id": payroll.employee_id,
        "month": payroll.month,
        "year": payroll.year,
        "baseSalary": payroll.basic_salary,
        "allowance": payroll.allowance,
        "grossSalary": payroll.brutto_salary,
        "bhxh": payroll.bhxh_amount,
        "bhyt": payroll.bhyt_amount,
        "incomeTax": payroll.tax_amount,
        "totalDeduction": payroll.total_deductions,
        "netSalary": payroll.netto_salary,
        "status": payroll.status.value,
        "notes": payroll.notes,
        "created_at": payroll.created_at.isoformat() if payroll.created_at else None
    }


def get_payroll_by_employee(employee_id, month=None, year=None):
    """Lấy bảng lương theo employee_id (khóa chính)."""
    query = Payroll.query.filter_by(employee_id=employee_id)

    if month:
        query = query.filter_by(month=month)
    if year:
        query = query.filter_by(year=year)

    payroll = query.order_by(Payroll.created_at.desc()).first()

    if not payroll:
        return None

    return {
        "baseSalary": payroll.basic_salary,
        "allowance": payroll.allowance,
        "grossSalary": payroll.brutto_salary,
        "bhxh": payroll.bhxh_amount,
        "bhyt": payroll.bhyt_amount,
        "incomeTax": payroll.tax_amount,
        "totalDeduction": payroll.total_deductions,
        "netSalary": payroll.netto_salary
    }


def calculate_payroll_for_month(month, year, created_by):
    """Tính lương cho tất cả nhân viên active trong tháng."""
    employees = Employee.query.filter_by(status='active').all()

    count = 0
    for emp in employees:
        calculate_payroll_for_one(emp.id, month, year, created_by)
        count += 1

    return {
        "message": f"Đã tính lương cho tháng {month}/{year}",
        "count": count
    }


def calculate_payroll_for_one(employee_id, month, year, created_by):
    """Tính lương cho 1 nhân viên cụ thể trong tháng và lưu/cập nhật kết quả."""
    emp = Employee.query.get(employee_id)
    if not emp:
        # Nếu truyền vào employee_id là dạng string (EMP001), hãy thử tìm theo code
        emp = Employee.query.filter_by(employee_id=employee_id).first()
        
    if not emp:
        raise ValueError("Nhân viên không tồn tại")

    # Kiểm tra/Truy tìm bản ghi lương cũ
    existing = Payroll.query.filter_by(
        employee_id=emp.id,
        month=month,
        year=year
    ).first()

    if existing:
        # Cập nhật lương cơ bản mới nhất từ hồ sơ
        existing.basic_salary = emp.basic_salary
        existing.calculate_payroll()
        existing.status = PayrollStatusEnum.CALCULATED
        existing.updated_at = datetime.utcnow()
        db.session.commit()
        return existing
    else:
        # Tạo mới
        payroll = Payroll(
            payroll_id=generate_id("PAY"),
            month=month,
            year=year,
            employee_id=emp.id,
            basic_salary=emp.basic_salary,
            allowance=0,
            created_by=created_by
        )
        payroll.calculate_payroll()
        payroll.status = PayrollStatusEnum.CALCULATED
        db.session.add(payroll)
        db.session.commit()
        return payroll


def create_payroll(data, created_by):
    """Tạo bảng lương cho một nhân viên cụ thể."""
    employee = Employee.query.get(data['employee_id'])
    if not employee:
        raise ValueError("Nhân viên không tồn tại")

    # Kiểm tra trùng lặp
    existing = Payroll.query.filter_by(
        employee_id=data['employee_id'],
        month=data['month'],
        year=data['year']
    ).first()

    if existing:
        raise ValueError(f"Bảng lương tháng {data['month']}/{data['year']} cho nhân viên này đã tồn tại")

    payroll = Payroll(
        payroll_id=generate_id("PAY"),
        month=data['month'],
        year=data['year'],
        employee_id=data['employee_id'],
        basic_salary=employee.basic_salary,
        allowance=data.get('allowance', 0),
        bhxh_rate=data.get('bhxh_rate', 0.08),
        bhyt_rate=data.get('bhyt_rate', 0.015),
        tax_rate=data.get('tax_rate', 0.05),
        deductions=data.get('deductions', 0),
        notes=data.get('notes', ''),
        created_by=created_by
    )
    payroll.calculate_payroll()
    payroll.status = PayrollStatusEnum.CALCULATED

    db.session.add(payroll)
    db.session.commit()

    return payroll


def update_payroll_status(payroll_id, status, user_id, note=None):
    """Cập nhật trạng thái bảng lương (duyệt, thanh toán, v.v.)."""
    payroll = Payroll.query.filter_by(payroll_id=payroll_id).first()

    if not payroll:
        raise ValueError("Bảng lương không tồn tại")

    status_enum_map = {
        "draft": PayrollStatusEnum.DRAFT,
        "calculated": PayrollStatusEnum.CALCULATED,
        "approved": PayrollStatusEnum.APPROVED,
        "paid": PayrollStatusEnum.PAID,
        # Vietnamese status names from frontend
        "Phê duyệt": PayrollStatusEnum.APPROVED,
        "Đã thanh toán": PayrollStatusEnum.PAID,
        "Chờ duyệt": PayrollStatusEnum.DRAFT,
        "Đã tính": PayrollStatusEnum.CALCULATED
    }

    new_status = status_enum_map.get(status)
    if not new_status:
        raise ValueError(f"Trạng thái không hợp lệ: {status}")

    payroll.status = new_status

    if new_status == PayrollStatusEnum.APPROVED:
        payroll.approved_by = user_id
        payroll.approved_at = datetime.utcnow()

    if new_status == PayrollStatusEnum.PAID:
        payroll.paid_by = user_id
        payroll.paid_at = datetime.utcnow()

    if note:
        payroll.notes = note

    payroll.updated_at = datetime.utcnow()
    db.session.commit()

    return payroll


def delete_payroll(payroll_id):
    """Xóa bảng lương (chỉ cho phép xóa khi ở trạng thái DRAFT hoặc CALCULATED)."""
    payroll = Payroll.query.filter_by(payroll_id=payroll_id).first()

    if not payroll:
        raise ValueError("Bảng lương không tồn tại")

    if payroll.status in (PayrollStatusEnum.APPROVED, PayrollStatusEnum.PAID):
        raise ValueError("Không thể xóa bảng lương đã được duyệt hoặc đã thanh toán")

    db.session.delete(payroll)
    db.session.commit()

    return True
