"""JWT and token authentication middleware."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.models.user import User


def token_required(f):
    """
    Decorator to protect routes with JWT authentication.
    Injects the current_user as the first argument to the decorated function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({'success': False, 'message': 'Authentication required. ' + str(e)}), 401

        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))

        if not current_user:
            return jsonify({'success': False, 'message': 'User not found.'}), 401
        if not current_user.is_active:
            return jsonify({'success': False, 'message': 'Account is deactivated. Please contact admin.'}), 403

        return f(current_user, *args, **kwargs)
    return decorated


def get_current_user():
    """Get the current authenticated user (call inside a jwt_required context)."""
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))
