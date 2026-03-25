from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from backend.routes.authentication_route import auth_bp
from backend.routes.cash_in_routes import cash_in_bp
from backend.routes.cash_out_routes import cash_out_bp
from backend.routes.employee_route import employees_bp
from backend.routes.user_route import users_bp
from backend.routes.export_routes import export_bp
from backend.routes.home_routes import home_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.payroll_routes import payroll_bp
from backend.routes.report_routes import report_bp
from backend.routes.account_routes import account_bp

from backend.models import db



def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost:3306/finance_management"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = "*-EI>6!Bl67#0>_N,{S_>{Y=LRl[#1}x?DXT%+}HUnT"
    db.init_app(app)
    JWTManager(app)
    CORS(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(cash_in_bp)
    app.register_blueprint(cash_out_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp)
    # app.register_blueprint(payroll_bp) # wait, frontend calls it /api/payroll, but employees_bp is already /api/employees. 
    # Actually frontend api.ts: getPayrollStats -> /api/payroll/stats. So payroll_bp is correct.
    app.register_blueprint(payroll_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(account_bp)


    @app.route("/")
    def home():
        return {
            "message": "Financial API Running",
            "status": "OK"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)