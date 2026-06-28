from datetime import datetime

from backend.enums.role_users import RoleEnum
from backend.models import User,db


def get_users(page, limit, status=None, role=None):

    query = User.query.filter(User.deleted_at.is_(None))

    if status:
        query = query.filter_by(status=status)

    if role:
        query = query.filter_by(role=RoleEnum[role.upper()])

    query = query.order_by(User.created_at.desc())

    total = query.count()
    users = query.paginate(page=page, per_page=limit)

    return users, total


def get_user(user_id):
    return User.query.get(user_id)


def create_user(data):

    user = User(
        username=data['username'],
        email=data['email'],
        full_name=data['full_name'],
        role=RoleEnum[data.get('role', 'VIEWER').upper()],
        department=data.get('department'),
        phone=data.get('phone'),
        status='active'
    )

    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return user


def update_user(user, data):

    if 'full_name' in data:
        user.full_name = data['full_name']

    if 'phone' in data:
        user.phone = data['phone']

    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url']

    if 'department' in data:
        user.department = data['department']

    user.updated_at = datetime.utcnow()

    db.session.commit()

    return user


def soft_delete_user(user):

    user.deleted_at = datetime.utcnow()
    user.status = "deleted"

    db.session.commit()