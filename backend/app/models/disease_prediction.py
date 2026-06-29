"""
Smart Agro - Disease Prediction Model
=======================================
Records AI-based crop disease detection results for farmers.
"""

from datetime import datetime
from app import db


class DiseasePrediction(db.Model):
    """
    Stores results from the AI disease detection service.
    Each record links to the farmer and optionally to a specific crop.
    """
    __tablename__ = 'disease_predictions'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey('farmer_profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    crop_id = db.Column(
        db.Integer,
        db.ForeignKey('crops.id', ondelete='SET NULL'),
        nullable=True,
        comment='Optionally linked to a specific crop in the farmer\'s portfolio'
    )

    # Input
    image_url = db.Column(db.String(256), nullable=True, comment='Uploaded plant image path')
    crop_type = db.Column(db.String(100), nullable=True, comment='User-specified crop type')

    # AI results
    disease_name = db.Column(db.String(200), nullable=False)
    confidence_score = db.Column(
        db.Float,
        nullable=False,
        comment='Model confidence between 0.0 and 1.0'
    )
    severity = db.Column(
        db.Enum('low', 'medium', 'high', 'none', name='disease_severity'),
        nullable=True
    )
    treatment_suggestion = db.Column(db.Text, nullable=True)
    prevention_tips = db.Column(db.Text, nullable=True)
    organic_treatment = db.Column(db.Text, nullable=True)

    predicted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        """Serialize disease prediction to dictionary."""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'crop_id': self.crop_id,
            'image_url': self.image_url,
            'crop_type': self.crop_type,
            'disease_name': self.disease_name,
            'confidence_score': self.confidence_score,
            'severity': self.severity,
            'treatment_suggestion': self.treatment_suggestion,
            'prevention_tips': self.prevention_tips,
            'organic_treatment': self.organic_treatment,
            'predicted_at': self.predicted_at.isoformat() if self.predicted_at else None,
        }

    def __repr__(self) -> str:
        return f'<DiseasePrediction {self.disease_name} ({self.confidence_score:.0%})>'
