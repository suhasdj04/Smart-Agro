"""Role-based access control middleware."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.models.user import User


def role_required(*allowed_roles):
    """
    Decorator to restrict access to specific user roles.
    Usage:
        @role_required('admin')
        @role_required('farmer', 'expert')
    Injects current_user as first argument.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({'success': False, 'message': 'Authentication required.'}), 401

            user_id = get_jwt_identity()
            current_user = User.query.get(int(user_id))

            if not current_user:
                return jsonify({'success': False, 'message': 'User not found.'}), 401
            if not current_user.is_active:
                return jsonify({'success': False, 'message': 'Account is deactivated.'}), 403
            if current_user.role not in allowed_roles:
                return jsonify({
                    'success': False,
                    'message': f'Access denied. Required role: {", ".join(allowed_roles)}. Your role: {current_user.role}.'
                }), 403

            return f(current_user, *args, **kwargs)
        return decorated
    return decorator


def farmer_required(f):
    """Shortcut decorator for farmer-only routes."""
    return role_required('farmer')(f)


def expert_required(f):
    """Shortcut decorator for expert-only routes."""
    return role_required('expert')(f)


def bank_required(f):
    """Shortcut decorator for bank-only routes."""
    return role_required('bank')(f)


def admin_required(f):
    """Shortcut decorator for admin-only routes."""
    return role_required('admin')(f)
