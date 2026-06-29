"""
Smart Agro - Crop Price Model
==============================
Stores market prices for various crops, updated by admins or bank officers.
Farmers can view these to make informed selling decisions.
"""

from datetime import datetime, date as date_type
from decimal import Decimal
from app import db


class CropPrice(db.Model):
    """
    Market price record for a specific crop at a specific market.
    Prices are updated regularly to give farmers market intelligence.
    """
    __tablename__ = 'crop_prices'

    id = db.Column(db.Integer, primary_key=True)

    # Crop identification
    crop_name = db.Column(db.String(100), nullable=False, index=True)
    variety = db.Column(db.String(100), nullable=True)

    # Pricing info
    price_per_kg = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        comment='Price per kilogram in INR'
    )
    unit = db.Column(db.String(20), default='kg', nullable=False,
                     comment='Unit of measurement (kg, quintal, etc.)')

    # Market location
    market_name = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(50), nullable=True)

    # Date of price record
    date = db.Column(db.Date, default=date_type.today, nullable=False, index=True)

    # Who entered this data
    updated_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        comment='User ID who last updated this price'
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        """Serialize crop price to dictionary."""
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'variety': self.variety,
            'price_per_kg': float(self.price_per_kg) if self.price_per_kg else None,
            'unit': self.unit,
            'market_name': self.market_name,
            'state': self.state,
            'date': self.date.isoformat() if self.date else None,
            'updated_by': self.updated_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f'<CropPrice {self.crop_name} ₹{self.price_per_kg}/kg at {self.market_name}>'
