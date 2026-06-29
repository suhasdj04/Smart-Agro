"""
Smart Agro - Farmer Profile Model
==================================
Stores farmer-specific information linked to a User account.
"""

from datetime import datetime
from app import db


class FarmerProfile(db.Model):
    """
    Farmer profile extending the base User model.
    Holds farm-related details, personal info, and links to farming data.
    """
    __tablename__ = 'farmer_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
        index=True
    )

    # Farm information
    farm_name = db.Column(db.String(100), nullable=True)
    farm_location = db.Column(db.String(200), nullable=True)
    farm_size = db.Column(db.Float, nullable=True, comment='Size in acres')
    soil_type = db.Column(
        db.Enum('Sandy', 'Loamy', 'Clay', 'Silt', 'Peaty', 'Chalky', 'Other',
                name='soil_types'),
        nullable=True
    )

    # Personal information
    phone = db.Column(db.String(15), nullable=True)
    aadhaar = db.Column(db.String(12), nullable=True, comment='12-digit Aadhaar number')
    address = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.String(256), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    crops = db.relationship('Crop', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    loans = db.relationship('Loan', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    complaints = db.relationship('Complaint', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    queries = db.relationship('Query', backref='farmer', lazy='dynamic', cascade='all, delete-orphan')
    disease_predictions = db.relationship(
        'DiseasePrediction', backref='farmer', lazy='dynamic', cascade='all, delete-orphan'
    )
    recommendations = db.relationship(
        'Recommendation', backref='farmer', lazy='dynamic', cascade='all, delete-orphan'
    )

    def to_dict(self) -> dict:
        """Serialize farmer profile to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'farm_name': self.farm_name,
            'farm_location': self.farm_location,
            'farm_size': self.farm_size,
            'soil_type': self.soil_type,
            'phone': self.phone,
            'aadhaar': self.aadhaar,
            'address': self.address,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<FarmerProfile user_id={self.user_id} farm={self.farm_name}>'
