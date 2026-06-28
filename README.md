# Accounting System Backend

This is the backend for the Accounting System, providing RESTful APIs for managing financial transactions, payrolls, chart of accounts, and employee data. It is built with Python and Flask.

## Tech Stack

* **Framework:** Flask
* **Database:** MySQL
* **ORM:** SQLAlchemy (Flask-SQLAlchemy)
* **Authentication:** JWT (Flask-JWT-Extended)
* **CORS:** Flask-CORS

## Features

* **Authentication & Authorization:** Secure JWT-based login for users and staff.
* **Financial Transactions:** Management of Cash In and Cash Out transactions.
* **Accounting Core:** Chart of Accounts, Bank Accounts, and Journal Entries.
* **Payroll System:** Employee management and payroll processing.
* **Reports & Dashboards:** Endpoints for fetching financial summaries and dashboard statistics.
* **Data Export:** Export functionalities for financial records.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/haidepzai0305/Accounting_System_backend.git
   cd Accounting_System_backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have your requirements.txt generated if you haven't already: `pip freeze > requirements.txt`)*

4. **Configure Database:**
   Update the database URI in `backend/app.py` (or through environment variables if configured):
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost:3306/finance_management"
   ```
   Create the `finance_management` database in your MySQL server.

5. **Run the Application:**
   ```bash
   python -m backend.app
   ```
   The API will be accessible at `http://localhost:5000/`.

## Project Structure

* `backend/`: Contains the main application code.
  * `models/`: SQLAlchemy database models.
  * `routes/`: Flask Blueprint routes mapping to endpoints.
  * `services/`: Business logic.
  * `enums/`: Application enums.
  * `app.py`: Application entry point.
* `seed_data.py`: Script to populate the database with initial sample data.
