"""
Smart Agro - Crop Model
========================
Tracks crops planted by farmers, including growth status and harvest data.
"""

from datetime import datetime
from app import db


class Crop(db.Model):
    """
    Represents a crop grown by a farmer.
    Tracks planting, growth status, and harvest information.
    """
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey('farmer_profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # Crop details
    name = db.Column(db.String(100), nullable=False, comment='Common crop name (e.g., Wheat, Rice)')
    variety = db.Column(db.String(100), nullable=True, comment='Specific variety or cultivar')
    area_acres = db.Column(db.Float, nullable=True, comment='Area under cultivation in acres')

    # Timeline
    planting_date = db.Column(db.Date, nullable=True)
    expected_harvest_date = db.Column(db.Date, nullable=True)
    actual_harvest_date = db.Column(db.Date, nullable=True)

    # Status tracking
    status = db.Column(
        db.Enum('growing', 'harvested', 'failed', name='crop_status'),
        default='growing',
        nullable=False
    )

    # Media & notes
    image_url = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    disease_predictions = db.relationship(
        'DiseasePrediction', backref='crop', lazy='dynamic', cascade='all, delete-orphan'
    )

    def to_dict(self) -> dict:
        """Serialize crop record to dictionary."""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'name': self.name,
            'variety': self.variety,
            'area_acres': self.area_acres,
            'planting_date': self.planting_date.isoformat() if self.planting_date else None,
            'expected_harvest_date': (
                self.expected_harvest_date.isoformat() if self.expected_harvest_date else None
            ),
            'actual_harvest_date': (
                self.actual_harvest_date.isoformat() if self.actual_harvest_date else None
            ),
            'status': self.status,
            'image_url': self.image_url,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<Crop {self.name} ({self.status}) farmer_id={self.farmer_id}>'
