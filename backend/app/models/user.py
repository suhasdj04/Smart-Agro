"""
Smart Agro - User Model
=======================
Core authentication model representing all users in the system.
Roles: admin, farmer, expert, bank
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """
    Central user model used for authentication.
    Role-specific data is stored in separate profile tables (FarmerProfile, etc.)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(
        db.Enum('admin', 'farmer', 'expert', 'bank', name='user_roles'),
        nullable=False
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    # One-to-one profile relationships (each user has at most one role profile)
    farmer_profile = db.relationship(
        'FarmerProfile', backref='user', uselist=False, cascade='all, delete-orphan'
    )
    expert_profile = db.relationship(
        'ExpertProfile', backref='user', uselist=False, cascade='all, delete-orphan'
    )
    bank_profile = db.relationship(
        'BankProfile', backref='user', uselist=False, cascade='all, delete-orphan'
    )
    notifications = db.relationship(
        'Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan'
    )

    # ── Password Helpers ───────────────────────────────────────────────────────
    def set_password(self, password: str) -> None:
        """Hash and store the user's password using werkzeug PBKDF2."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    # ── Serialization ──────────────────────────────────────────────────────────
    def to_dict(self, include_profile: bool = False) -> dict:
        """Convert user to a JSON-serializable dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_profile:
            if self.role == 'farmer' and self.farmer_profile:
                data['profile'] = self.farmer_profile.to_dict()
            elif self.role == 'expert' and self.expert_profile:
                data['profile'] = self.expert_profile.to_dict()
            elif self.role == 'bank' and self.bank_profile:
                data['profile'] = self.bank_profile.to_dict()
            else:
                data['profile'] = None

        return data

    def __repr__(self) -> str:
        return f'<User {self.email} ({self.role})>'
