"""Authentication controller - business logic for auth routes."""
from flask import jsonify
from flask_jwt_extended import create_access_token
from app import db
from app.models.user import User
from app.models.farmer import FarmerProfile
from app.models.expert import ExpertProfile
from app.models.bank import BankProfile
from app.utils.response import success_response, error_response
from app.utils.validators import validate_email, validate_password, validate_required_fields
from app.services.notification_service import create_notification


def register_user(data):
    """Handle user registration."""
    if not data:
        return error_response('Request body is required.')

    # Validate required fields
    required = ['name', 'email', 'password', 'role']
    missing = validate_required_fields(data, required)
    if missing:
        return error_response(f'Missing required fields: {", ".join(missing)}')

    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    role = data.get('role', '').strip().lower()
    role_data = data.get('role_data', {})

    # Validate role
    valid_roles = ['farmer', 'expert', 'bank']
    if role not in valid_roles:
        return error_response(f'Invalid role. Must be one of: {", ".join(valid_roles)}')

    # Validate email
    is_valid_email, email_error = validate_email(email)
    if not is_valid_email:
        return error_response(f'Invalid email: {email_error}')

    # Validate password
    is_valid_pass, pass_error = validate_password(password)
    if not is_valid_pass:
        return error_response(pass_error)

    # Check email uniqueness
    if User.query.filter_by(email=email).first():
        return error_response('An account with this email already exists.', 409)

    try:
        # Create user
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Get user.id before committing

        # Create role-specific profile
        if role == 'farmer':
            profile = FarmerProfile(
                user_id=user.id,
                farm_name=role_data.get('farm_name', ''),
                farm_location=role_data.get('farm_location', ''),
                farm_size=role_data.get('farm_size'),
                soil_type=role_data.get('soil_type', 'Loamy'),
                phone=role_data.get('phone', ''),
                address=role_data.get('address', '')
            )
            db.session.add(profile)

        elif role == 'expert':
            profile = ExpertProfile(
                user_id=user.id,
                specialization=role_data.get('specialization', ''),
                qualification=role_data.get('qualification', ''),
                experience_years=role_data.get('experience_years', 0),
                phone=role_data.get('phone', '')
            )
            db.session.add(profile)

        elif role == 'bank':
            profile = BankProfile(
                user_id=user.id,
                bank_name=role_data.get('bank_name', ''),
                branch_name=role_data.get('branch_name', ''),
                ifsc_code=role_data.get('ifsc_code', ''),
                phone=role_data.get('phone', '')
            )
            db.session.add(profile)

        db.session.commit()

        # Create welcome notification
        create_notification(
            user.id,
            f'Welcome to Smart Agro, {name}!',
            'Your account has been created successfully. Explore AI-powered crop tools, weather insights, and more.',
            'success'
        )

        # Generate JWT token
        token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )

        return success_response(
            data={'token': token, 'user': user.to_dict()},
            message='Registration successful! Welcome to Smart Agro.',
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f'Registration failed: {str(e)}', 500)


def login_user(data):
    """Handle user login."""
    if not data:
        return error_response('Request body is required.')

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return error_response('Email and password are required.')

    user = User.query.filter_by(email=email).first()

    if not user:
        return error_response('Invalid email or password.', 401)

    if not user.check_password(password):
        return error_response('Invalid email or password.', 401)

    if not user.is_active:
        return error_response('Your account has been deactivated. Please contact admin.', 403)

    # Generate JWT token
    token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role}
    )

    return success_response(
        data={'token': token, 'user': user.to_dict()},
        message=f'Welcome back, {user.name}!'
    )


def logout_user():
    """Handle logout (JWT is stateless; client removes token)."""
    return success_response(message='Logged out successfully.')


def get_current_user_info(current_user):
    """Return current authenticated user's full profile."""
    user_dict = current_user.to_dict()

    # Include role-specific profile
    if current_user.role == 'farmer' and current_user.farmer_profile:
        user_dict['profile'] = current_user.farmer_profile.to_dict()
    elif current_user.role == 'expert' and current_user.expert_profile:
        user_dict['profile'] = current_user.expert_profile.to_dict()
    elif current_user.role == 'bank' and current_user.bank_profile:
        user_dict['profile'] = current_user.bank_profile.to_dict()

    return success_response(data=user_dict)


def change_password(current_user, data):
    """Handle password change."""
    if not data:
        return error_response('Request body is required.')

    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')

    if not current_password or not new_password:
        return error_response('Current password and new password are required.')

    if not current_user.check_password(current_password):
        return error_response('Current password is incorrect.', 401)

    is_valid, error_msg = validate_password(new_password)
    if not is_valid:
        return error_response(error_msg)

    if current_password == new_password:
        return error_response('New password must be different from the current password.')

    try:
        current_user.set_password(new_password)
        db.session.commit()
        return success_response(message='Password changed successfully.')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to change password: {str(e)}', 500)
