from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.models import User
from backend.services.user_service import get_users, create_user, get_user, update_user, soft_delete_user
from backend.utils.audit_log import create_audit_log
from backend.utils.permission import check_admin

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

from backend.models import db

@users_bp.route('', methods=['GET'])
@jwt_required()
def users_list():

    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not check_admin(current_user):
        return jsonify({"message": "Forbidden"}), 403

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)

    users, total = get_users(page, limit)

    return jsonify({
        "status": "success",
        "data": {
            "users": [u.to_dict() for u in users.items],
            "total": total
        }
    })

@users_bp.route('/stats', methods=['GET'])
@jwt_required()
def user_stats():
    # Only allow admin
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not check_admin(current_user):
        return jsonify({"message": "Forbidden"}), 403

    total_users = User.query.count()
    active_roles = db.session.query(User.role).distinct().count()
    
    return jsonify({
        "status": "success",
        "data": {
            "totalUsers": total_users,
            "activeRoles": active_roles,
            "pendingApprovals": 0
        }
    })

@users_bp.route('', methods=['POST'])
@jwt_required()
def create():

    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not check_admin(admin):
        return jsonify({"message": "Forbidden"}), 403

    data = request.get_json()

    user = create_user(data)

    create_audit_log(admin_id, "create", "users", user.id, None, user.to_dict())

    return jsonify(user.to_dict()), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update(user_id):

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    user = get_user(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    old_data = user.to_dict()

    user = update_user(user, data)

    create_audit_log(current_user_id, "update", "users", user.id, old_data, user.to_dict())

    return jsonify(user.to_dict())

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete(user_id):

    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not check_admin(admin):
        return jsonify({"message": "Forbidden"}), 403

    user = get_user(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    old_data = user.to_dict()

    soft_delete_user(user)

    create_audit_log(admin_id, "delete", "users", user.id, old_data, None)

    return jsonify({"message": "User deleted"})