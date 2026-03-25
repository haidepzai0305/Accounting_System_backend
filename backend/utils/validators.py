import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):

    if len(password) < 8:
        return False, "Mật khẩu phải có ít nhất 8 ký tự"

    if not re.search(r'[A-Z]', password):
        return False, "Mật khẩu phải chứa ít nhất 1 chữ hoa"

    if not re.search(r'[0-9]', password):
        return False, "Mật khẩu phải chứa ít nhất 1 số"

    if not re.search(r'[!@#$%^&*]', password):
        return False, "Mật khẩu phải chứa ít nhất 1 ký tự đặc biệt"

    return True, "OK"