"""
Smart Agro - Auth Service
==========================
Business logic for authentication operations.
"""

from app import db
from app.models.user import User
from app.models.farmer import FarmerProfile
from app.models.expert import ExpertProfile
from app.models.bank import BankProfile
from app.services.notification_service import create_notification


def create_user_with_profile(
    name: str,
    email: str,
    password: str,
    role: str,
    role_data: dict = None
) -> tuple:
    """
    Create a User and its corresponding role profile in a single transaction.

    Args:
        name:      Full name of the user.
        email:     Unique email address.
        password:  Plaintext password (will be hashed).
        role:      One of 'admin', 'farmer', 'expert', 'bank'.
        role_data: Optional dict with profile-specific fields.

    Returns:
        Tuple of (user: User, error: str or None)
    """
    role_data = role_data or {}

    # Check email uniqueness
    if User.query.filter_by(email=email).first():
        return None, 'A user with this email already exists.'

    # Create user record
    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()  # Get user.id without committing

    # Create role-specific profile
    if role == 'farmer':
        profile = FarmerProfile(
            user_id=user.id,
            farm_name=role_data.get('farm_name'),
            farm_location=role_data.get('farm_location'),
            phone=role_data.get('phone'),
        )
        db.session.add(profile)

    elif role == 'expert':
        profile = ExpertProfile(
            user_id=user.id,
            specialization=role_data.get('specialization'),
            qualification=role_data.get('qualification'),
            phone=role_data.get('phone'),
        )
        db.session.add(profile)

    elif role == 'bank':
        profile = BankProfile(
            user_id=user.id,
            bank_name=role_data.get('bank_name'),
            branch_name=role_data.get('branch_name'),
            ifsc_code=role_data.get('ifsc_code'),
            phone=role_data.get('phone'),
        )
        db.session.add(profile)

    # Send welcome notification (no separate commit, handled below)
    welcome_notif = create_notification(
        user_id=user.id,
        title='Welcome to Smart Agro! 🌾',
        message=(
            f'Hello {name}, welcome to Smart Agro — your AI-powered agriculture '
            'management platform. Explore the dashboard to get started!'
        ),
        notification_type='success',
        commit=False
    )

    db.session.commit()
    return user, None
