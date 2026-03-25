CREATE DATABASE finance_management;
USE finance_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin','accountant','manager','viewer') DEFAULT 'viewer',
    department VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'active',
    last_login_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME
);

CREATE TABLE chart_of_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    type ENUM('asset','liability','equity','revenue','expense') NOT NULL,
    category VARCHAR(50),
    description TEXT,
    balance BIGINT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    parent_account_code VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (parent_account_code) REFERENCES chart_of_accounts(code)
);

CREATE TABLE bank_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    account_number VARCHAR(50) UNIQUE NOT NULL,
    account_holder VARCHAR(100) NOT NULL,
    balance BIGINT DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'VND',
    account_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    last_reconciled_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE cash_in_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    date DATE NOT NULL,
    amount BIGINT NOT NULL,
    currency VARCHAR(3) DEFAULT 'VND',
    source VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    account_debit VARCHAR(20) NOT NULL,
    account_credit VARCHAR(20) NOT NULL,
    status ENUM('pending','approved','rejected') DEFAULT 'pending',
    approved_by INT,
    approved_at DATETIME,
    rejection_reason VARCHAR(500),
    notes VARCHAR(500),
    created_by INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (account_debit) REFERENCES chart_of_accounts(code),
    FOREIGN KEY (account_credit) REFERENCES chart_of_accounts(code),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
CREATE TABLE cash_out_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    date DATE NOT NULL,
    amount BIGINT NOT NULL,
    currency VARCHAR(3) DEFAULT 'VND',
    category VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    bank_account_id INT,
    account_debit VARCHAR(20) NOT NULL,
    account_credit VARCHAR(20) NOT NULL,
    status ENUM('pending','approved','rejected') DEFAULT 'pending',
    approved_by INT,
    approved_at DATETIME,
    rejection_reason VARCHAR(500),
    notes VARCHAR(500),
    created_by INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id),
    FOREIGN KEY (account_debit) REFERENCES chart_of_accounts(code),
    FOREIGN KEY (account_credit) REFERENCES chart_of_accounts(code),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    identification_number VARCHAR(20),
    phone VARCHAR(20),
    email VARCHAR(100),
    department VARCHAR(100) NOT NULL,
    position VARCHAR(100),
    basic_salary BIGINT NOT NULL,
    join_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE payroll (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payroll_id VARCHAR(50) UNIQUE NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    employee_id INT NOT NULL,
    basic_salary BIGINT NOT NULL,
    allowance BIGINT DEFAULT 0,
    bhxh_rate FLOAT DEFAULT 0.08,
    bhxh_amount BIGINT DEFAULT 0,
    bhyt_rate FLOAT DEFAULT 0.015,
    bhyt_amount BIGINT DEFAULT 0,
    tax_rate FLOAT DEFAULT 0.05,
    tax_amount BIGINT DEFAULT 0,
    deductions BIGINT DEFAULT 0,
    status ENUM('draft','calculated','approved','paid') DEFAULT 'draft',
    approved_by INT,
    approved_at DATETIME,
    payment_date DATE,
    paid_by INT,
    paid_at DATETIME,
    transaction_id VARCHAR(50),
    notes VARCHAR(500),
    created_by INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (approved_by) REFERENCES users(id),
    FOREIGN KEY (paid_by) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (transaction_id) REFERENCES cash_out_detail(transaction_id)
);

CREATE TABLE insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    insurance_id VARCHAR(50) UNIQUE NOT NULL,
    employee_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    provider VARCHAR(100),
    policy_number VARCHAR(100),
    coverage_amount BIGINT,
    status VARCHAR(20) DEFAULT 'active',
    effective_date DATE,
    expiry_date DATE,
    payment_method VARCHAR(50),
    employee_contribution_rate FLOAT,
    employer_contribution_rate FLOAT,
    notes VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE journal_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    journal_id VARCHAR(50) UNIQUE NOT NULL,
    transaction_id VARCHAR(50),
    period VARCHAR(10),
    date DATE NOT NULL,
    description VARCHAR(500) NOT NULL,
    account_debit VARCHAR(20) NOT NULL,
    account_credit VARCHAR(20) NOT NULL,
    amount BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    is_system_generated BOOLEAN DEFAULT TRUE,
    reference_id INT,
    posted_by INT,
    posted_at DATETIME,
    notes VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (account_debit) REFERENCES chart_of_accounts(code),
    FOREIGN KEY (account_credit) REFERENCES chart_of_accounts(code),
    FOREIGN KEY (posted_by) REFERENCES users(id)
);

CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    period  VARCHAR(10),
    title VARCHAR(200) NOT NULL,
    data JSON,
    summary JSON,
    status VARCHAR(20) DEFAULT 'draft',
    generated_by INT NOT NULL,
    generated_at DATETIME,
    published_by INT,
    published_at DATETIME,
    file_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (generated_by) REFERENCES users(id),
    FOREIGN KEY (published_by) REFERENCES users(id)
);

CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_id VARCHAR(50) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id VARCHAR(50),
    old_value JSON,
    new_value JSON,
    change_summary VARCHAR(500),
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),
    status_code INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE attachments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_id VARCHAR(50) UNIQUE NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(20) NOT NULL,
    file_size INT NOT NULL,
    s3_key VARCHAR(500),
    transaction_id VARCHAR(50),
    related_table VARCHAR(50),
    related_id VARCHAR(50),
    uploaded_by INT NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME,

    FOREIGN KEY (transaction_id) REFERENCES cash_in_detail(transaction_id),
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);


