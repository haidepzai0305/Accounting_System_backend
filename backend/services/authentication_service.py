from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

import uuid

from backend.models import AuditLog, db, User
from backend.utils.validators import validate_email, validate_password


def create_audit_log(user_id, action, table_name, record_id=None, old_value=None, new_value=None):

    log = AuditLog(
        log_id=f"LOG{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4]}",
        user_id=user_id,
        action=action,
        table_name=table_name,
        record_id=record_id,
        old_value=old_value,
        new_value=new_value,
        timestamp=datetime.utcnow()
    )

    db.session.add(log)
    db.session.commit()


def login_service(data):
    username = data.get('username') or data.get('email')
    
    if not username:
        return None, "MISSING_IDENTIFIER"

    user = User.query.filter_by(username=username).first()
    
    # If not found by username, try searching by email
    if not user:
        user = User.query.filter_by(email=username).first()

    if not user or not user.check_password(data.get('password')):
        return None, "INVALID_CREDENTIAL"

    if user.status != "active":
        return None, "ACCOUNT_DISABLED"

    user.last_login_at = datetime.utcnow()
    db.session.commit()

    token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=24)
    )

    create_audit_log(user.id, "login", "users", user.id)

    return {
        "accessToken": token,
        "user": user.to_dict(),
        "expiresIn": 86400
    }, None


def register_service(data, RoleEnum):

    if not data:
        return None, "INVALID_REQUEST"

    email = data.get("email")
    password = data.get("password")
    username = data.get("username") or data.get("email") # Fallback to email if username is missing
    full_name = data.get("full_name") or data.get("name") or "" # Fallback to name if full_name is missing

    if not email or not password or not username:
        return None, "MISSING_REQUIRED_FIELDS"

    if not validate_email(email):
        return None, "INVALID_EMAIL"

    is_valid, message = validate_password(password)
    if not is_valid:
        return None, message

    if User.query.filter_by(email=email).first():
        return None, "EMAIL_EXISTS"

    if User.query.filter_by(username=username).first():
        return None, "USERNAME_EXISTS"

    # Handle role - default to viewer for public registration
    role_raw = data.get("role")
    if not role_raw:
        role_enum = RoleEnum.viewer
    else:
        role_input = str(role_raw).lower().strip()
        try:
            # Try finding role by name (e.g. "admin", "viewer")
            role_enum = RoleEnum[role_input]
        except KeyError:
            # Fallback: Try finding role by value (e.g. "admin", "viewer")
            try:
                role_enum = RoleEnum(role_input)
            except ValueError:
                # If explicitly invalid role provided, default to viewer for safety
                role_enum = RoleEnum.viewer

    try:
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            role=role_enum,
            status="active"
        )

        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        try:
            create_audit_log(
                user.id,
                "create",
                "users",
                user.id,
                None,
                user.to_dict()
            )
        except:
            pass

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "message": "Đăng ký thành công"
        }, None

    except Exception as e:
        db.session.rollback()
        return None, str(e)