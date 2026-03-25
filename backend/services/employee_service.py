from datetime import datetime

from backend.models.Employee import Employee , db


def get_employees(page, limit, status=None, department=None):
    query = Employee.query

    if status:
        query = query.filter_by(status=status)

    if department:
        query = query.filter_by(department=department)

    query = query.order_by(Employee.created_at.desc())

    total = query.count()
    employees = query.paginate(page=page, per_page=limit)

    return employees, total


def get_employee(employee_id):
    return Employee.query.get(employee_id)


def create_employee(data):
    employee = Employee(
        employee_id=data['employee_id'],
        full_name=data['full_name'],
        department=data['department'],
        basic_salary=data['basic_salary'],
        join_date=datetime.strptime(data['join_date'], '%Y-%m-%d').date(),
        status=data.get('status', 'active')
    )

    db.session.add(employee)
    db.session.commit()

    return employee


def update_employee(employee, data):
    if 'full_name' in data:
        employee.full_name = data['full_name']

    if 'phone' in data:
        employee.phone = data['phone']

    if 'email' in data:
        employee.email = data['email']

    if 'position' in data:
        employee.position = data['position']

    if 'basic_salary' in data:
        employee.basic_salary = data['basic_salary']

    if 'status' in data:
        employee.status = data['status']

    employee.updated_at = datetime.utcnow()

    db.session.commit()

    return employee