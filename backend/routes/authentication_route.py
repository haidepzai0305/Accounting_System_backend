from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.enums.role_users import RoleEnum
from backend.models import User
from backend.services.authentication_service import login_service, register_service

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    result, error = login_service(data)

    if error == "INVALID_CREDENTIAL":
        return jsonify({
            "status": "error",
            "message": "Username hoặc password không chính xác"
        }), 401

    if error == "ACCOUNT_DISABLED":
        return jsonify({
            "status": "error",
            "message": "Tài khoản bị vô hiệu hóa"
        }), 403

    return jsonify({
        "status": "success",
        "data": result
    })


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body phải là JSON"
        }), 400

    result, error = register_service(data, RoleEnum)

    if error == "INVALID_EMAIL":
        return jsonify({"status": "error", "message": "Email không hợp lệ"}), 400

    if error == "EMAIL_EXISTS":
        return jsonify({"status": "error", "message": "Email đã tồn tại"}), 409

    if error == "USERNAME_EXISTS":
        return jsonify({"status": "error", "message": "Username đã tồn tại"}), 409

    if error:
        return jsonify({"status": "error", "message": error}), 400

    return jsonify({
        "status": "success",
        "data": result
    }), 201


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": user.to_dict()
    })
