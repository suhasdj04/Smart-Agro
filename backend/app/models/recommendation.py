"""
Smart Agro - Recommendation Model
====================================
Stores AI-generated recommendations for crops, fertilizers, and yields.
"""

import json
from datetime import datetime
from app import db


class Recommendation(db.Model):
    """
    Stores AI recommendation results (crop, fertilizer, yield predictions).
    Both input_data and result are stored as JSON for flexibility.
    """
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey('farmer_profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Type of recommendation
    type = db.Column(
        db.Enum('crop', 'fertilizer', 'yield', name='recommendation_types'),
        nullable=False,
        index=True
    )

    # Raw input parameters (JSON)
    input_data = db.Column(db.Text, nullable=True, comment='JSON-encoded input parameters')

    # AI/ML result (JSON)
    result = db.Column(db.Text, nullable=False, comment='JSON-encoded recommendation result')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # ── JSON helpers ───────────────────────────────────────────────────────────
    def get_input_data(self) -> dict:
        """Parse JSON input_data field."""
        if self.input_data:
            try:
                return json.loads(self.input_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def get_result(self) -> dict:
        """Parse JSON result field."""
        if self.result:
            try:
                return json.loads(self.result)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}

    def set_input_data(self, data: dict) -> None:
        """Serialize dict to JSON for storage."""
        self.input_data = json.dumps(data)

    def set_result(self, data: dict) -> None:
        """Serialize dict to JSON for storage."""
        self.result = json.dumps(data)

    def to_dict(self) -> dict:
        """Serialize recommendation to dictionary."""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'type': self.type,
            'input_data': self.get_input_data(),
            'result': self.get_result(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f'<Recommendation [{self.type}] farmer_id={self.farmer_id}>'
