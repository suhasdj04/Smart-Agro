"""Authentication routes."""
from flask import Blueprint, request
from app.middleware.auth_middleware import token_required
from app.controllers.auth_controller import (
    register_user, login_user, logout_user,
    get_current_user_info, change_password
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    return register_user(request.get_json())


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and receive JWT token."""
    return login_user(request.get_json())


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout (client-side token removal)."""
    return logout_user()


@auth_bp.route('/me', methods=['GET'])
@token_required
def me(current_user):
    """Get the currently authenticated user's info."""
    return get_current_user_info(current_user)


@auth_bp.route('/me/password', methods=['PUT'])
@token_required
def update_password(current_user):
    """Change the current user's password."""
    return change_password(current_user, request.get_json())
