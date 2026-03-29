import sys
sys.path.insert(0, '.')
from backend.app import app

with app.app_context():
    from backend.extension import db
    from backend.enums.PayrollStatus import PayrollStatusEnum

    # Check what SQLAlchemy Enum expects vs what's in DB
    print("Enum members:", list(PayrollStatusEnum))
    print("Enum names:", [e.name for e in PayrollStatusEnum])
    print("Enum values:", [e.value for e in PayrollStatusEnum])

    # Check DB statuses
    result = db.session.execute(db.text("SELECT DISTINCT status FROM payroll"))
    rows = result.fetchall()
    db_statuses = [row[0] for row in rows]
    print("DB statuses:", db_statuses)

    # By default, SQLAlchemy Enum uses .name not .value
    # So in DB it expects DRAFT, CALCULATED, APPROVED, PAID  (uppercase names)
    # But the DB has draft, calculated, approved, paid (lowercase values)

    # The db schema uses: ENUM('draft','calculated','approved','paid')
    # which stores lowercase values
    # But SQLAlchemy db.Enum(PayrollStatusEnum) by default uses .name (DRAFT, CALCULATED...)
    # unless values_callable is specified

    # This mismatch causes the error!
    print()
    print("DIAGNOSIS: SQLAlchemy Enum by default matches against member NAMES (DRAFT, CALCULATED, etc.)")
    print("But the database stores VALUES (draft, calculated, etc.)")
    print("Need to set values_callable=lambda e: [x.value for x in e] in the Column definition")
