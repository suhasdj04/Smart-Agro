"""
Smart Agro - Complaint Model
==============================
Allows farmers to raise complaints which are handled by admins.
"""

from datetime import datetime
from app import db


class Complaint(db.Model):
    """
    Complaint raised by a farmer regarding any aspect of the agricultural system.
    Admins review and resolve complaints.
    """
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey('farmer_profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Complaint content
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Categorization
    category = db.Column(
        db.Enum('crop', 'loan', 'weather', 'expert', 'other', name='complaint_categories'),
        default='other',
        nullable=False
    )
    priority = db.Column(
        db.Enum('low', 'medium', 'high', name='complaint_priority'),
        default='medium',
        nullable=False
    )

    # Status & resolution
    status = db.Column(
        db.Enum('open', 'in_progress', 'resolved', 'closed', name='complaint_status'),
        default='open',
        nullable=False,
        index=True
    )
    admin_reply = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self) -> dict:
        """Serialize complaint to dictionary."""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'subject': self.subject,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'admin_reply': self.admin_reply,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<Complaint #{self.id} [{self.status}] {self.subject[:30]}>'
