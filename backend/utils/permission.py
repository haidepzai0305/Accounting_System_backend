from backend.enums.role_users import RoleEnum


def check_admin(user):
    return user.role == RoleEnum.ADMIN