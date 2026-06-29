"""
Smart Agro - Query Model
=========================
Farmer-to-Expert query system for agricultural advice.
Farmers submit questions, experts provide answers.
"""

from datetime import datetime
from app import db


class Query(db.Model):
    """
    Represents a question submitted by a farmer to an agricultural expert.
    Queries go through open → answered → closed lifecycle.
    """
    __tablename__ = 'queries'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey('farmer_profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    expert_id = db.Column(
        db.Integer,
        db.ForeignKey('expert_profiles.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        comment='Assigned expert (null until an expert picks it up)'
    )

    # Query content
    subject = db.Column(db.String(200), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True, comment='Expert\'s answer')

    # Classification
    category = db.Column(
        db.Enum('disease', 'fertilizer', 'pesticide', 'irrigation', 'general',
                name='query_categories'),
        default='general',
        nullable=False,
        index=True
    )

    # Status tracking
    status = db.Column(
        db.Enum('open', 'answered', 'closed', name='query_status'),
        default='open',
        nullable=False,
        index=True
    )

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    answered_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self) -> dict:
        """Serialize query to dictionary."""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'expert_id': self.expert_id,
            'subject': self.subject,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'answered_at': self.answered_at.isoformat() if self.answered_at else None,
        }

    def __repr__(self) -> str:
        return f'<Query #{self.id} [{self.status}] {self.subject[:40]}>'
