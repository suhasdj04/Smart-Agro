"""Input validation utilities."""
import re
from email_validator import validate_email as _validate_email, EmailNotValidError


def validate_email(email):
    """Validate email format. Returns (is_valid, error_message)."""
    try:
        _validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)


def validate_password(password):
    """
    Validate password strength.
    Must be at least 8 chars, contain 1 uppercase and 1 digit.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain at least one uppercase letter.'
    if not re.search(r'\d', password):
        return False, 'Password must contain at least one digit.'
    return True, None


def validate_required_fields(data, required_fields):
    """
    Check that all required fields are present and non-empty.
    Returns list of missing/empty field names.
    """
    missing = []
    for field in required_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    return missing


def validate_phone(phone):
    """Validate Indian phone number format."""
    pattern = r'^[6-9]\d{9}$'
    return bool(re.match(pattern, str(phone).strip()))


def validate_ifsc(ifsc):
    """Validate IFSC code format."""
    pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
    return bool(re.match(pattern, str(ifsc).strip().upper()))
