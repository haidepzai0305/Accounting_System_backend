# -*- coding: utf-8 -*-
"""
Seed script - uses raw SQL INSERT IGNORE to avoid ORM enum deserialization issues.
Run from the project root:
    .venv\\Scripts\\python.exe seed_data.py
"""
from datetime import date, datetime
from backend.app import create_app
from backend.extension import db
from backend.extension.db import bcrypt


def run_seed():
    app = create_app()
    with app.app_context():
        print("Starting database seed...")

        # ---------------------------------------------------------------
        # 1. Chart of Accounts
        # ---------------------------------------------------------------
        print("  Seeding chart_of_accounts...")
        coa_rows = [
            ("111", "Tien mat",                      "asset",     "Tien",        150000000),
            ("112", "Tien gui ngan hang",             "asset",     "Tien",        850000000),
            ("131", "Phai thu khach hang",            "asset",     "Phai thu",    45000000),
            ("152", "Nguyen vat lieu",                "asset",     "Hang ton kho",30000000),
            ("331", "Phai tra nha cung cap",          "liability", "Phai tra",    20000000),
            ("334", "Phai tra nguoi lao dong",        "liability", "Phai tra",    120000000),
            ("338", "Phai tra khac BHXH BHYT",        "liability", "Phai tra",    15000000),
            ("411", "Von dau tu chu so huu",          "equity",    "Von",         1000000000),
            ("511", "Doanh thu ban hang",             "revenue",   "Doanh thu",   0),
            ("515", "Doanh thu tai chinh",            "revenue",   "Doanh thu",   0),
            ("621", "Chi phi nguyen vat lieu",        "expense",   "Chi phi",     0),
            ("622", "Chi phi nhan cong",              "expense",   "Chi phi",     0),
            ("627", "Chi phi san xuat chung",         "expense",   "Chi phi",     0),
            ("641", "Chi phi ban hang",               "expense",   "Chi phi",     0),
            ("642", "Chi phi quan ly doanh nghiep",   "expense",   "Chi phi",     0),
        ]
        count = 0
        for code, name, typ, cat, bal in coa_rows:
            result = db.session.execute(
                db.text("INSERT IGNORE INTO chart_of_accounts (code, name, type, category, balance) VALUES (:code, "
                        ":name, :type, :cat, :bal)"),
                {"code": code, "name": name, "type": typ, "cat": cat, "bal": bal}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 2. Bank Accounts
        # ---------------------------------------------------------------
        print("  Seeding bank_accounts...")
        bank_rows = [
            ("Vietcombank",  "0071001234567",  "Cong Ty TNHH ABC", 500000000,  "VND", "checking", "active"),
            ("Techcombank",  "19033456789012", "Cong Ty TNHH ABC", 250000000,  "VND", "savings",  "active"),
            ("BIDV",         "12010003456789", "Cong Ty TNHH ABC", 100000000,  "VND", "checking", "active"),
        ]
        count = 0
        for bank_name, acc_no, holder, bal, cur, acc_type, status in bank_rows:
            result = db.session.execute(
                db.text("INSERT IGNORE INTO bank_accounts (bank_name, account_number, account_holder, balance, currency, account_type, status) VALUES (:bn, :an, :ah, :bal, :cur, :at, :st)"),
                {"bn": bank_name, "an": acc_no, "ah": holder, "bal": bal, "cur": cur, "at": acc_type, "st": status}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 3. Users  (need bcrypt hashing)
        # ---------------------------------------------------------------
        print("  Seeding users...")
        users_data = [
            ("admin",     "admin@company.com",     "Nguyen Van Admin",  "admin",       "Ban Giam Doc",   "0901234567"),
            ("ketoan01",  "ketoan01@company.com",  "Tran Thi Ke Toan",  "accountant",  "Phong Ke Toan",  "0912345678"),
            ("manager01", "manager01@company.com", "Le Van Quan Ly",    "manager",     "Phong Nhan Su",  "0923456789"),
            ("viewer01",  "viewer01@company.com",  "Pham Thi Xem",      "viewer",      "Phong Ky Thuat", "0934567890"),
            ("ketoan02",  "ketoan02@company.com",  "Hoang Minh Tu",     "accountant",  "Phong Ke Toan",  "0945678901"),
        ]
        count = 0
        for uname, email, fname, role, dept, phone in users_data:
            existing = db.session.execute(
                db.text("SELECT id FROM users WHERE username = :u"), {"u": uname}
            ).fetchone()
            if existing:
                continue
            pw_hash = bcrypt.generate_password_hash("password123").decode("utf-8")
            db.session.execute(
                db.text("INSERT INTO users (username, email, password_hash, full_name, role, department, phone, status) VALUES (:u, :e, :ph, :fn, :r, :d, :p, 'active')"),
                {"u": uname, "e": email, "ph": pw_hash, "fn": fname, "r": role, "d": dept, "p": phone}
            )
            count += 1
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # Get user IDs
        ketoan_id  = db.session.execute(db.text("SELECT id FROM users WHERE username='ketoan01'")).scalar()
        manager_id = db.session.execute(db.text("SELECT id FROM users WHERE username='manager01'")).scalar()
        print("    ketoan01 id={}, manager01 id={}".format(ketoan_id, manager_id))

        # ---------------------------------------------------------------
        # 4. Employees
        # ---------------------------------------------------------------
        print("  Seeding employees...")
        emp_rows = [
            ("EMP001", "Nguyen Thi Lan",  "1990-03-15", "female", "001090003456", "0901111111", "lan@company.com",  "Phong Ke Toan",  "Ke Toan Vien",          12000000, "2020-06-01", "active"),
            ("EMP002", "Tran Van Hung",   "1988-07-22", "male",   "001088007891", "0902222222", "hung@company.com", "Phong Ky Thuat", "Ky Su Phan Mem",        18000000, "2019-03-10", "active"),
            ("EMP003", "Le Thi Mai",      "1995-11-05", "female", "001095011234", "0903333333", "mai@company.com",  "Phong Nhan Su",  "Chuyen Vien Nhan Su",   11000000, "2021-08-15", "active"),
            ("EMP004", "Pham Quoc Bao",   "1985-01-30", "male",   "001085001567", "0904444444", "bao@company.com",  "Ban Giam Doc",   "Truong Phong",          30000000, "2015-04-20", "active"),
            ("EMP005", "Hoang Thi Thu",   "1993-05-18", "female", "001093005678", "0905555555", "thu@company.com",  "Phong Marketing","Chuyen Vien MKT",       13000000, "2022-01-05", "active"),
            ("EMP006", "Vu Minh Khoa",    "1991-09-10", "male",   "001091009012", "0906666666", "khoa@company.com", "Phong Ky Thuat", "Ky Su Cap Cao",         22000000, "2018-10-01", "active"),
            ("EMP007", "Dang Thi Hoa",    "1997-02-14", "female", "001097002345", "0907777777", "hoa@company.com",  "Phong Ke Toan",  "Ke Toan Tong Hop",      14000000, "2023-03-20", "active"),
            ("EMP008", "Bui Van Nam",     "1983-12-03", "male",   "001083012678", "0908888888", "nam@company.com",  "Phong Bao Ve",   "Bao Ve",                 7000000, "2017-07-01", "inactive"),
        ]
        count = 0
        for eid, fname, dob, gender, idn, phone, email, dept, pos, sal, jdate, status in emp_rows:
            result = db.session.execute(
                db.text("""INSERT IGNORE INTO employees
                    (employee_id, full_name, date_of_birth, gender, identification_number,
                     phone, email, department, position, basic_salary, join_date, status)
                    VALUES (:eid,:fn,:dob,:gen,:idn,:ph,:em,:dept,:pos,:sal,:jd,:st)"""),
                {"eid": eid, "fn": fname, "dob": dob, "gen": gender, "idn": idn,
                 "ph": phone, "em": email, "dept": dept, "pos": pos, "sal": sal,
                 "jd": jdate, "st": status}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 5. Cash In
        # ---------------------------------------------------------------
        print("  Seeding cash_in_detail...")
        cash_in_rows = [
            ("CI-2026-001", "2026-01-05", 50000000,  "Hoc phi", "Thu hoc phi ky 1 2025-2026",   "112","511","APPROVED", manager_id,"2026-01-05 10:30:00", None,  ketoan_id),
            ("CI-2026-002", "2026-01-15", 25000000,  "Quy",     "Nhan ho tro tu quy phuc loi",  "112","515","APPROVED", manager_id,"2026-01-15 14:00:00", None,  ketoan_id),
            ("CI-2026-003", "2026-02-03", 80000000,  "Hoc phi", "Thu hoc phi ky 2 2025-2026",   "112","511","APPROVED", manager_id,"2026-02-03 09:00:00", None,  ketoan_id),
            ("CI-2026-004", "2026-02-20", 10000000,  "Khac",    "Ban thanh ly tai san cu",       "111","511","APPROVED", manager_id,"2026-02-20 11:00:00", None,  ketoan_id),
            ("CI-2026-005", "2026-03-01", 60000000,  "Hoc phi", "Thu hoc phi thang 3",           "112","511","PENDING",  None,      None,                  None,  ketoan_id),
            ("CI-2026-006", "2026-03-10", 15000000,  "Quy",     "Nhan tai tro tu doi tac",       "112","515","PENDING",  None,      None,                  None,  ketoan_id),
            ("CI-2025-012", "2025-12-05", 45000000,  "Hoc phi", "Thu hoc phi thang 12-2025",     "112","511","APPROVED", manager_id,"2025-12-05 10:00:00", None,  ketoan_id),
            ("CI-2025-011", "2025-11-10", 30000000,  "Khac",    "Thu hoi cong no khach hang",    "112","131","REJECTED", None,      None,  "Chung tu khong hop le", ketoan_id),
        ]
        count = 0
        for txn_id, dt, amt, src, desc, dr, cr, status, appr_by, appr_at, rej, cby in cash_in_rows:
            result = db.session.execute(
                db.text("""INSERT IGNORE INTO cash_in_detail
                    (transaction_id, date, amount, currency, source, description,
                     account_debit, account_credit, status, approved_by, approved_at,
                     rejection_reason, created_by)
                    VALUES (:tid,:dt,:amt,'VND',:src,:desc,:dr,:cr,:st,:ab,:aa,:rej,:cby)"""),
                {"tid": txn_id, "dt": dt, "amt": amt, "src": src, "desc": desc,
                 "dr": dr, "cr": cr, "st": status, "ab": appr_by, "aa": appr_at,
                 "rej": rej, "cby": cby}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 6. Cash Out
        # ---------------------------------------------------------------
        print("  Seeding cash_out_detail...")
        bank_id = db.session.execute(db.text("SELECT id FROM bank_accounts WHERE bank_name='Vietcombank'")).scalar()
        cash_out_rows = [
            ("CO-2026-001","2026-01-31",120000000,"Luong",   "Tra luong thang 01-2026",         bank_id,"334","112","APPROVED",manager_id,"2026-01-31 15:00:00",ketoan_id),
            ("CO-2026-002","2026-02-05",8500000,  "Bao tri", "Bao tri dieu hoa van phong",      bank_id,"627","112","APPROVED",manager_id,"2026-02-05 10:00:00",ketoan_id),
            ("CO-2026-003","2026-02-28",120000000,"Luong",   "Tra luong thang 02-2026",         bank_id,"334","112","APPROVED",manager_id,"2026-02-28 15:00:00",ketoan_id),
            ("CO-2026-004","2026-03-02",15000000, "Mua sam", "Mua thiet bi van phong moi",      bank_id,"641","112","APPROVED",manager_id,"2026-03-02 09:30:00",ketoan_id),
            ("CO-2026-005","2026-03-10",5000000,  "Bao tri", "Sua chua may tinh nhan vien",     bank_id,"627","111","PENDING", None,     None,                  ketoan_id),
            ("CO-2026-006","2026-03-15",120000000,"Luong",   "Tra luong thang 03-2026",         bank_id,"334","112","PENDING", None,     None,                  ketoan_id),
            ("CO-2025-012","2025-12-31",120000000,"Luong",   "Tra luong thang 12-2025",         bank_id,"334","112","APPROVED",manager_id,"2025-12-31 15:00:00",ketoan_id),
            ("CO-2025-011","2025-11-20",20000000, "Mua sam", "Mua phan mem ban quyen",          bank_id,"642","112","APPROVED",manager_id,"2025-11-20 11:00:00",ketoan_id),
        ]
        count = 0
        for txn_id, dt, amt, cat, desc, bid, dr, cr, status, appr_by, appr_at, cby in cash_out_rows:
            result = db.session.execute(
                db.text("""INSERT IGNORE INTO cash_out_detail
                    (transaction_id, date, amount, currency, category, description,
                     bank_account_id, account_debit, account_credit,
                     status, approved_by, approved_at, created_by)
                    VALUES (:tid,:dt,:amt,'VND',:cat,:desc,:bid,:dr,:cr,:st,:ab,:aa,:cby)"""),
                {"tid": txn_id, "dt": dt, "amt": amt, "cat": cat, "desc": desc,
                 "bid": bid, "dr": dr, "cr": cr, "st": status,
                 "ab": appr_by, "aa": appr_at, "cby": cby}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 7. Payroll
        # ---------------------------------------------------------------
        print("  Seeding payroll...")
        employees = db.session.execute(
            db.text("SELECT id, employee_id, full_name, basic_salary, department, status FROM employees")
        ).fetchall()
        active_emps = [e for e in employees if e.status == "active"]

        periods = [
            (2025, 12, "paid",     "CO-2025-012", "2025-12-25 14:00:00", "2025-12-28 10:00:00", "2025-12-28"),
            (2026, 1,  "paid",     "CO-2026-001", "2026-01-25 14:00:00", "2026-01-28 10:00:00", "2026-01-28"),
            (2026, 2,  "approved", "CO-2026-003", "2026-02-25 14:00:00", None,                  None),
            (2026, 3,  "draft",    None,           None,                  None,                  None),
        ]

        count = 0
        for month, year, status, txn_id, appr_at, paid_at, pay_date in periods:
            for emp in active_emps:
                payroll_id = "PR-{}{:02d}-{}".format(year, month, emp.employee_id)
                exists = db.session.execute(
                    db.text("SELECT id FROM payroll WHERE payroll_id=:pid"), {"pid": payroll_id}
                ).fetchone()
                if exists:
                    continue

                basic = emp.basic_salary
                allowance = 1500000 if emp.department == "Phong Ky Thuat" else 1000000
                bhxh = int(basic * 0.08)
                bhyt = int(basic * 0.015)
                tax  = int((basic + allowance) * 0.05)
                appr_by = manager_id if status in ("approved", "paid") else None
                paid_by = manager_id if status == "paid" else None

                db.session.execute(
                    db.text("""INSERT IGNORE INTO payroll
                        (payroll_id, month, year, employee_id, basic_salary, allowance,
                         bhxh_rate, bhxh_amount, bhyt_rate, bhyt_amount, tax_rate, tax_amount,
                         deductions, status, approved_by, approved_at, payment_date,
                         paid_by, paid_at, transaction_id, notes, created_by)
                        VALUES
                        (:pid,:mo,:yr,:eid,:bs,:al,
                         0.08,:bhxh,0.015,:bhyt,0.05,:tax,
                         0,:st,:ab,:aa,:pd,
                         :pb,:paid,:tid,:notes,:cby)"""),
                    {
                        "pid": payroll_id, "mo": month, "yr": year,
                        "eid": emp.id, "bs": basic, "al": allowance,
                        "bhxh": bhxh, "bhyt": bhyt, "tax": tax,
                        "st": status, "ab": appr_by, "aa": appr_at,
                        "pd": pay_date, "pb": paid_by, "paid": paid_at,
                        "tid": txn_id,
                        "notes": "Bang luong thang {}/{} - {}".format(month, year, emp.full_name),
                        "cby": ketoan_id
                    }
                )
                count += 1
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 8. Insurance
        # ---------------------------------------------------------------
        print("  Seeding insurance...")
        insurance_rows = [
            # (insurance_id, employee_id_col, type, provider, policy_number, coverage_amount, status, effective_date, expiry_date, payment_method, emp_rate, employer_rate, notes)
            ("INS-EMP001-BHXH", "EMP001", "BHXH", "BHXH Viet Nam", "BHXH-2020-001", 0,       "active", "2020-06-01", "2026-12-31", "monthly", 0.08, 0.17, "Bao hiem xa hoi bat buoc"),
            ("INS-EMP001-BHYT", "EMP001", "BHYT", "BHYT Viet Nam", "BHYT-2020-001", 0,       "active", "2020-06-01", "2026-12-31", "monthly", 0.015, 0.03, "Bao hiem y te bat buoc"),
            ("INS-EMP002-BHXH", "EMP002", "BHXH", "BHXH Viet Nam", "BHXH-2019-002", 0,       "active", "2019-03-10", "2026-12-31", "monthly", 0.08, 0.17, "Bao hiem xa hoi bat buoc"),
            ("INS-EMP002-BHYT", "EMP002", "BHYT", "BHYT Viet Nam", "BHYT-2019-002", 0,       "active", "2019-03-10", "2026-12-31", "monthly", 0.015, 0.03, "Bao hiem y te bat buoc"),
            ("INS-EMP003-BHXH", "EMP003", "BHXH", "BHXH Viet Nam", "BHXH-2021-003", 0,       "active", "2021-08-15", "2026-12-31", "monthly", 0.08, 0.17, "Bao hiem xa hoi bat buoc"),
            ("INS-EMP003-BHYT", "EMP003", "BHYT", "BHYT Viet Nam", "BHYT-2021-003", 0,       "active", "2021-08-15", "2026-12-31", "monthly", 0.015, 0.03, "Bao hiem y te bat buoc"),
            ("INS-EMP004-BHXH", "EMP004", "BHXH", "BHXH Viet Nam", "BHXH-2015-004", 0,       "active", "2015-04-20", "2026-12-31", "monthly", 0.08, 0.17, "Bao hiem xa hoi bat buoc"),
            ("INS-EMP004-BHYT", "EMP004", "BHYT", "BHYT Viet Nam", "BHYT-2015-004", 0,       "active", "2015-04-20", "2026-12-31", "monthly", 0.015, 0.03, "Bao hiem y te bat buoc"),
            ("INS-EMP004-NLD",  "EMP004", "Bao hiem nhan tho", "Bao Viet",    "BV-2015-004",  500000000, "active", "2015-04-20", "2026-04-19", "annual",  0.0,  0.0, "Bao hiem nhan tho cho lanh dao"),
            ("INS-EMP005-BHXH", "EMP005", "BHXH", "BHXH Viet Nam", "BHXH-2022-005", 0,       "active", "2022-01-05", "2026-12-31", "monthly", 0.08, 0.17, "Bao hiem xa hoi bat buoc"),
            ("INS-EMP005-BHYT", "EMP005", "BHYT", "BHYT Viet Nam", "BHYT-2022-005", 0,       "active", "2022-01-05", "2026-12-31", "monthly", 0.015, 0.03, "Bao hiem y te bat buoc"),
            ("INS-EMP006-BHXH", "EMP006", "BHXH", "BHXH Viet Nam", "BHXH-2018-006", 0,       "active", "2018-10-01", "2026-12-31", "monthly", 0.08, 0.17, "Bao hiem xa hoi bat buoc"),
            ("INS-EMP006-BHYT", "EMP006", "BHYT", "BHYT Viet Nam", "BHYT-2018-006", 0,       "active", "2018-10-01", "2026-12-31", "monthly", 0.015, 0.03, "Bao hiem y te bat buoc"),
            ("INS-EMP007-BHXH", "EMP007", "BHXH", "BHXH Viet Nam", "BHXH-2023-007", 0,       "active", "2023-03-20", "2026-12-31", "monthly", 0.08, 0.17, "Bao hiem xa hoi bat buoc"),
            ("INS-EMP007-BHYT", "EMP007", "BHYT", "BHYT Viet Nam", "BHYT-2023-007", 0,       "active", "2023-03-20", "2026-12-31", "monthly", 0.015, 0.03, "Bao hiem y te bat buoc"),
            ("INS-EMP008-BHXH", "EMP008", "BHXH", "BHXH Viet Nam", "BHXH-2017-008", 0,       "inactive","2017-07-01", "2025-12-31", "monthly", 0.08, 0.17, "Bao hiem da ngung do nghi viec"),
        ]
        count = 0
        for ins_id, emp_code, ins_type, provider, policy, coverage, status, eff, exp, pay_method, emp_rate, emr_rate, notes in insurance_rows:
            emp_id_val = db.session.execute(
                db.text("SELECT id FROM employees WHERE employee_id = :eid"), {"eid": emp_code}
            ).scalar()
            if emp_id_val is None:
                continue
            result = db.session.execute(
                db.text("""INSERT IGNORE INTO insurance
                    (insurance_id, employee_id, type, provider, policy_number, coverage_amount,
                     status, effective_date, expiry_date, payment_method,
                     employee_contribution_rate, employer_contribution_rate, notes)
                    VALUES (:iid,:eid,:typ,:prov,:pol,:cov,:st,:eff,:exp,:pm,:er,:emr,:notes)"""),
                {"iid": ins_id, "eid": emp_id_val, "typ": ins_type, "prov": provider,
                 "pol": policy, "cov": coverage, "st": status, "eff": eff, "exp": exp,
                 "pm": pay_method, "er": emp_rate, "emr": emr_rate, "notes": notes}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 9. Journal Entries
        # ---------------------------------------------------------------
        print("  Seeding journal_entries...")
        admin_id = db.session.execute(db.text("SELECT id FROM users WHERE username='admin'")).scalar()
        journal_rows = [
            # (journal_id, transaction_id, period, date, description, debit, credit, amount, status, posted_by, posted_at)
            ("JE-2026-001", "CI-2026-001", "2026-01", "2026-01-05", "Ghi nhan thu hoc phi ky 1",        "112","511", 50000000, "posted", admin_id, "2026-01-05 11:00:00"),
            ("JE-2026-002", "CI-2026-002", "2026-01", "2026-01-15", "Ghi nhan thu ho tro quy phuc loi", "112","515", 25000000, "posted", admin_id, "2026-01-15 14:30:00"),
            ("JE-2026-003", "CO-2026-001", "2026-01", "2026-01-31", "Ghi nhan tra luong T01-2026",       "334","112",120000000, "posted", admin_id, "2026-01-31 16:00:00"),
            ("JE-2026-004", "CI-2026-003", "2026-02", "2026-02-03", "Ghi nhan thu hoc phi ky 2",        "112","511", 80000000, "posted", admin_id, "2026-02-03 09:30:00"),
            ("JE-2026-005", "CO-2026-002", "2026-02", "2026-02-05", "Ghi nhan chi bao tri dieu hoa",    "627","112",  8500000, "posted", admin_id, "2026-02-05 10:30:00"),
            ("JE-2026-006", "CI-2026-004", "2026-02", "2026-02-20", "Ghi nhan ban thanh ly tai san",    "111","511", 10000000, "posted", admin_id, "2026-02-20 11:30:00"),
            ("JE-2026-007", "CO-2026-003", "2026-02", "2026-02-28", "Ghi nhan tra luong T02-2026",       "334","112",120000000, "posted", admin_id, "2026-02-28 16:00:00"),
            ("JE-2026-008", "CO-2026-004", "2026-03", "2026-03-02", "Ghi nhan mua thiet bi van phong",  "641","112", 15000000, "posted", admin_id, "2026-03-02 10:00:00"),
            ("JE-2026-009", "CI-2026-005", "2026-03", "2026-03-01", "Ghi nhan thu hoc phi T03 (tam)",   "112","511", 60000000, "draft",  None,      None),
            ("JE-2026-010", "CI-2026-006", "2026-03", "2026-03-10", "Ghi nhan nhan tai tro doi tac",    "112","515", 15000000, "draft",  None,      None),
            ("JE-2025-001", "CI-2025-012", "2025-12", "2025-12-05", "Ghi nhan thu hoc phi T12-2025",    "112","511", 45000000, "posted", admin_id, "2025-12-05 10:30:00"),
            ("JE-2025-002", "CO-2025-012", "2025-12", "2025-12-31", "Ghi nhan tra luong T12-2025",      "334","112",120000000, "posted", admin_id, "2025-12-31 16:00:00"),
            ("JE-2025-003", "CO-2025-011", "2025-11", "2025-11-20", "Ghi nhan mua phan mem ban quyen",  "642","112", 20000000, "posted", admin_id, "2025-11-20 11:30:00"),
        ]
        count = 0
        for jid, tid, period, dt, desc, dr, cr, amt, status, posted_by, posted_at in journal_rows:
            result = db.session.execute(
                db.text("""INSERT IGNORE INTO journal_entries
                    (journal_id, transaction_id, period, date, description,
                     account_debit, account_credit, amount, status,
                     is_system_generated, posted_by, posted_at)
                    VALUES (:jid,:tid,:per,:dt,:desc,:dr,:cr,:amt,:st,TRUE,:pb,:pa)"""),
                {"jid": jid, "tid": tid, "per": period, "dt": dt, "desc": desc,
                 "dr": dr, "cr": cr, "amt": amt, "st": status,
                 "pb": posted_by, "pa": posted_at}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 10. Reports
        # ---------------------------------------------------------------
        print("  Seeding reports...")
        import json
        report_rows = [
            (
                "RPT-2025-12-CF", "cash_flow", "2025-12", "Bao cao luong tien thang 12/2025",
                json.dumps({"total_in": 45000000, "total_out": 140000000, "net": -95000000}),
                json.dumps({"status": "deficit", "note": "Chi luong cao"}),
                "published", admin_id, "2026-01-05 09:00:00", admin_id, "2026-01-06 10:00:00"
            ),
            (
                "RPT-2026-01-CF", "cash_flow", "2026-01", "Bao cao luong tien thang 01/2026",
                json.dumps({"total_in": 75000000, "total_out": 120000000, "net": -45000000}),
                json.dumps({"status": "deficit", "note": "Chi luong va hanh chinh"}),
                "published", ketoan_id, "2026-02-03 09:00:00", manager_id, "2026-02-04 10:00:00"
            ),
            (
                "RPT-2026-02-CF", "cash_flow", "2026-02", "Bao cao luong tien thang 02/2026",
                json.dumps({"total_in": 90000000, "total_out": 128500000, "net": -38500000}),
                json.dumps({"status": "deficit", "note": "Doanh thu tang nhe"}),
                "published", ketoan_id, "2026-03-03 09:00:00", manager_id, "2026-03-04 10:00:00"
            ),
            (
                "RPT-2026-03-CF", "cash_flow", "2026-03", "Bao cao luong tien thang 03/2026 (tam)",
                json.dumps({"total_in": 75000000, "total_out": 140000000, "net": -65000000}),
                json.dumps({"status": "draft"}),
                "draft", ketoan_id, "2026-03-15 09:00:00", None, None
            ),
            (
                "RPT-2025-Q4-PL", "payroll", "2025-Q4", "Bao cao luong Quy 4/2025",
                json.dumps({"total_employees": 7, "total_salary": 360000000, "total_bhxh": 28800000, "total_bhyt": 5400000, "total_tax": 18300000}),
                json.dumps({"avg_salary": 17142857, "highest_dept": "Ban Giam Doc"}),
                "published", ketoan_id, "2026-01-10 10:00:00", manager_id, "2026-01-11 10:00:00"
            ),
            (
                "RPT-2026-Q1-PL", "payroll", "2026-Q1", "Bao cao luong Quy 1/2026 (tam)",
                json.dumps({"total_employees": 7, "total_salary": 720000000, "total_bhxh": 57600000, "total_bhyt": 10800000, "total_tax": 36600000}),
                json.dumps({"avg_salary": 17142857, "note": "Chua bao gom thang 3"}),
                "draft", ketoan_id, "2026-03-15 14:00:00", None, None
            ),
        ]
        count = 0
        for rid, rtype, period, title, data, summary, status, gen_by, gen_at, pub_by, pub_at in report_rows:
            result = db.session.execute(
                db.text("""INSERT IGNORE INTO reports
                    (report_id, type, period, title, data, summary, status,
                     generated_by, generated_at, published_by, published_at)
                    VALUES (:rid,:rt,:per,:tit,:dat,:sum,:st,:gb,:ga,:pb,:pa)"""),
                {"rid": rid, "rt": rtype, "per": period, "tit": title,
                 "dat": data, "sum": summary, "st": status,
                 "gb": gen_by, "ga": gen_at, "pb": pub_by, "pa": pub_at}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 11. Audit Logs
        # ---------------------------------------------------------------
        print("  Seeding audit_logs...")
        viewer_id = db.session.execute(db.text("SELECT id FROM users WHERE username='viewer01'")).scalar()
        audit_rows = [
            # (log_id, user_id, action, table_name, record_id, old_val, new_val, summary, ip, status_code, ts)
            ("LOG-001", admin_id,    "LOGIN",  "users",           str(admin_id),    None, None,                                              "Admin dang nhap he thong",              "192.168.1.1",  200, "2026-03-20 08:00:00"),
            ("LOG-002", ketoan_id,   "LOGIN",  "users",           str(ketoan_id),   None, None,                                              "Ke toan dang nhap he thong",            "192.168.1.10", 200, "2026-03-20 08:05:00"),
            ("LOG-003", ketoan_id,   "CREATE", "cash_in_detail",  "CI-2026-005",    None, json.dumps({"transaction_id":"CI-2026-005","amount":60000000}), "Tao phieu thu CI-2026-005", "192.168.1.10", 201, "2026-03-20 08:30:00"),
            ("LOG-004", ketoan_id,   "CREATE", "cash_in_detail",  "CI-2026-006",    None, json.dumps({"transaction_id":"CI-2026-006","amount":15000000}), "Tao phieu thu CI-2026-006", "192.168.1.10", 201, "2026-03-20 09:00:00"),
            ("LOG-005", manager_id,  "UPDATE", "cash_in_detail",  "CI-2026-001",    json.dumps({"status":"pending"}), json.dumps({"status":"approved"}), "Phe duyet phieu thu CI-2026-001", "192.168.1.20", 200, "2026-01-05 10:30:00"),
            ("LOG-006", manager_id,  "UPDATE", "cash_out_detail", "CO-2026-001",    json.dumps({"status":"pending"}), json.dumps({"status":"approved"}), "Phe duyet phieu chi CO-2026-001", "192.168.1.20", 200, "2026-01-31 15:00:00"),
            ("LOG-007", ketoan_id,   "CREATE", "payroll",         "PR-202601-EMP001", None, json.dumps({"payroll_id":"PR-202601-EMP001","amount":12000000}), "Tao bang luong T01/2026 NV EMP001", "192.168.1.10", 201, "2026-01-20 10:00:00"),
            ("LOG-008", admin_id,    "CREATE", "reports",         "RPT-2026-01-CF", None, json.dumps({"report_id":"RPT-2026-01-CF"}),        "Tao bao cao luong tien T01/2026",       "192.168.1.1",  201, "2026-02-03 09:00:00"),
            ("LOG-009", viewer_id,   "VIEW",   "reports",         "RPT-2026-01-CF", None, None,                                              "Xem bao cao T01/2026",                  "192.168.1.50", 200, "2026-02-05 14:00:00"),
            ("LOG-010", ketoan_id,   "UPDATE", "cash_in_detail",  "CI-2025-011",    json.dumps({"status":"pending"}), json.dumps({"status":"rejected","rejection_reason":"Chung tu khong hop le"}), "Tu choi phieu thu CI-2025-011", "192.168.1.10", 200, "2025-11-15 09:00:00"),
            ("LOG-011", manager_id,  "LOGIN",  "users",           str(manager_id),  None, None,                                              "Quan ly dang nhap he thong",            "192.168.1.20", 200, "2026-03-20 08:10:00"),
            ("LOG-012", ketoan_id,   "CREATE", "journal_entries", "JE-2026-008",    None, json.dumps({"journal_id":"JE-2026-008"}),          "Ghi so but toan mua thiet bi",          "192.168.1.10", 201, "2026-03-02 10:00:00"),
        ]
        count = 0
        for lid, uid, action, tblname, rec_id, old_v, new_v, summary, ip, sc, ts in audit_rows:
            result = db.session.execute(
                db.text("""INSERT IGNORE INTO audit_logs
                    (log_id, user_id, action, table_name, record_id,
                     old_value, new_value, change_summary, ip_address, status_code, timestamp)
                    VALUES (:lid,:uid,:act,:tbl,:rid,:ov,:nv,:sum,:ip,:sc,:ts)"""),
                {"lid": lid, "uid": uid, "act": action, "tbl": tblname,
                 "rid": rec_id, "ov": old_v, "nv": new_v, "sum": summary,
                 "ip": ip, "sc": sc, "ts": ts}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        # 12. Attachments
        # ---------------------------------------------------------------
        print("  Seeding attachments...")
        attachment_rows = [
            # (file_id, original_filename, file_type, file_size_bytes, s3_key, transaction_id, related_table, related_id, uploaded_by)
            ("FILE-001", "phieu_thu_CI2026001.pdf",    "pdf",  245760, "uploads/2026/01/CI-2026-001/phieu_thu.pdf",     "CI-2026-001", "cash_in_detail",  "CI-2026-001", ketoan_id),
            ("FILE-002", "bien_lai_CI2026001.jpg",     "jpg",   98304, "uploads/2026/01/CI-2026-001/bien_lai.jpg",      "CI-2026-001", "cash_in_detail",  "CI-2026-001", ketoan_id),
            ("FILE-003", "phieu_thu_CI2026002.pdf",    "pdf",  221184, "uploads/2026/01/CI-2026-002/phieu_thu.pdf",     "CI-2026-002", "cash_in_detail",  "CI-2026-002", ketoan_id),
            ("FILE-004", "phieu_chi_CO2026001.pdf",    "pdf",  266240, "uploads/2026/01/CO-2026-001/phieu_chi.pdf",     "CI-2026-001", "cash_out_detail", "CO-2026-001", ketoan_id),
            ("FILE-005", "bang_luong_T01_2026.xlsx",  "xlsx",  40960, "uploads/2026/01/payroll/bang_luong_01_2026.xlsx", None,         "payroll",         "PR-202601",   ketoan_id),
            ("FILE-006", "phieu_thu_CI2026003.pdf",    "pdf",  258048, "uploads/2026/02/CI-2026-003/phieu_thu.pdf",     "CI-2026-003", "cash_in_detail",  "CI-2026-003", ketoan_id),
            ("FILE-007", "hoa_don_bao_tri_CO2026002.pdf","pdf",184320, "uploads/2026/02/CO-2026-002/hoa_don.pdf",       "CI-2026-001", "cash_out_detail", "CO-2026-002", ketoan_id),
            ("FILE-008", "hop_dong_mua_sam_CO2026004.pdf","pdf",327680,"uploads/2026/03/CO-2026-004/hop_dong.pdf",      "CI-2026-001", "cash_out_detail", "CO-2026-004", ketoan_id),
            ("FILE-009", "bao_cao_CF_T01_2026.pdf",   "pdf",  512000, "uploads/reports/RPT-2026-01-CF.pdf",            None,          "reports",         "RPT-2026-01-CF", admin_id),
            ("FILE-010", "bao_cao_luong_Q4_2025.pdf", "pdf",  450560, "uploads/reports/RPT-2025-Q4-PL.pdf",            None,          "reports",         "RPT-2025-Q4-PL", admin_id),
        ]
        count = 0
        for fid, orig_name, ftype, fsize, s3key, tid, rel_tbl, rel_id, uploader in attachment_rows:
            result = db.session.execute(
                db.text("""INSERT IGNORE INTO attachments
                    (file_id, original_filename, file_type, file_size, s3_key,
                     transaction_id, related_table, related_id, uploaded_by)
                    VALUES (:fid,:fn,:ft,:fs,:s3,:tid,:rtbl,:rid,:uid)"""),
                {"fid": fid, "fn": orig_name, "ft": ftype, "fs": fsize,
                 "s3": s3key, "tid": tid, "rtbl": rel_tbl, "rid": rel_id, "uid": uploader}
            )
            count += result.rowcount
        db.session.commit()
        print("    -> {} rows inserted.".format(count))

        # ---------------------------------------------------------------
        print("\n===================================================")
        print("Seed complete! All mock data has been inserted.")
        print("===================================================")
        print("\nDefault login (all passwords: password123):")
        print("  admin      -> role: admin")
        print("  ketoan01   -> role: accountant")
        print("  manager01  -> role: manager")
        print("  viewer01   -> role: viewer")


if __name__ == "__main__":
    run_seed()
