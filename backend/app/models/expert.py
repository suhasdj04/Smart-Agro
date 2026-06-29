"""
Smart Agro - Expert Profile Model
===================================
Stores agricultural expert details linked to a User account.
Experts answer farmer queries and provide guidance.
"""

from datetime import datetime
from app import db


class ExpertProfile(db.Model):
    """
    Expert profile extending the base User model.
    Agricultural experts can answer farmer queries and provide guidance.
    """
    __tablename__ = 'expert_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
        index=True
    )

    # Professional information
    specialization = db.Column(db.String(100), nullable=True,
                               comment='e.g., Soil Science, Crop Protection, Irrigation')
    qualification = db.Column(db.String(200), nullable=True,
                              comment='Highest degree/certification')
    experience_years = db.Column(db.Integer, default=0, nullable=True,
                                 comment='Years of professional experience')
    bio = db.Column(db.Text, nullable=True, comment='Short professional biography')

    # Contact details
    phone = db.Column(db.String(15), nullable=True)
    profile_image = db.Column(db.String(256), nullable=True)

    # Availability flag (experts can mark themselves unavailable)
    is_available = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    queries = db.relationship('Query', backref='expert', lazy='dynamic')

    def to_dict(self) -> dict:
        """Serialize expert profile to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'specialization': self.specialization,
            'qualification': self.qualification,
            'experience_years': self.experience_years,
            'bio': self.bio,
            'phone': self.phone,
            'profile_image': self.profile_image,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<ExpertProfile user_id={self.user_id} specialization={self.specialization}>'
