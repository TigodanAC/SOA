import re
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


def validate_login(login):
    if not re.match(r"^[A-Za-z0-9_-]{3,20}$", login):
        return False, "Login can only contain letters, numbers, underscores, hyphens"

    if 5 <= len(login) <= 15:
        return True, ""
    else:
        return False, "Login must be from 5 to 15 characters long"


def validate_email_format(email):
    try:
        validate_email(email, check_deliverability=False)
        return True, ""
    except EmailNotValidError:
        return False, "Invalid email format"


def validate_password(password):
    if len(password) < 4:
        return False, "Password must be at least 4 characters long"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    return True, ""


def validate_name(name):
    if re.match(r"^[A-Za-z'-]+$", name):
        return True, ""
    else:
        return False, "Name can only contain letters, apostrophes, hyphens"


def validate_date_of_birth(date_str):
    try:
        if datetime.fromisoformat(date_str) > datetime.now():
            return False, "Date of birth cannot be in the future"
        return True, ""
    except ValueError:
        return False, "Invalid date format"
