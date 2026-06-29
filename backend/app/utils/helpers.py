"""General helper utilities."""
import uuid
import random
import string
from datetime import datetime


def paginate_query(query, page, per_page=10):
    """Paginate a SQLAlchemy query. Returns (items, total)."""
    page = max(1, int(page))
    per_page = min(max(1, int(per_page)), 100)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total


def format_datetime(dt):
    """Format datetime to ISO string."""
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def format_date(d):
    """Format date to DD/MM/YYYY string."""
    if d is None:
        return None
    return d.strftime('%d/%m/%Y')


def generate_loan_reference():
    """Generate a unique loan reference number like LOAN-2024-XXXXX."""
    year = datetime.utcnow().year
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f'LOAN-{year}-{suffix}'


def generate_unique_filename(original_filename):
    """Generate a UUID-based unique filename preserving the extension."""
    ext = original_filename.rsplit('.', 1)[-1].lower() if '.' in original_filename else 'jpg'
    return f'{uuid.uuid4().hex}.{ext}'


def allowed_file(filename, allowed_extensions=None):
    """Check if file has an allowed extension."""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
