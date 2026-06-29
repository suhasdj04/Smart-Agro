"""
Smart Agro - Notification Model
=================================
System notifications sent to users for important events.
"""

from datetime import datetime
from app import db


class Notification(db.Model):
    """
    In-app notification sent to users for events like loan approvals,
    query answers, complaint updates, etc.
    """
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Notification content
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # Type controls the UI color/icon displayed
    type = db.Column(
        db.Enum('info', 'success', 'warning', 'error', name='notification_types'),
        default='info',
        nullable=False
    )

    # Read status
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        """Serialize notification to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f'<Notification user={self.user_id} [{self.type}] {self.title[:40]}>'
