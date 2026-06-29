"""
Smart Agro - Bank Profile Model
================================
Stores bank/financial institution details for loan officers.
"""

from datetime import datetime
from app import db


class BankProfile(db.Model):
    """
    Bank profile extending the base User model.
    Represents a bank officer who manages loan applications from farmers.
    """
    __tablename__ = 'bank_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
        index=True
    )

    # Bank/Branch details
    bank_name = db.Column(db.String(100), nullable=True,
                          comment='Name of the bank (e.g., State Bank of India)')
    branch_name = db.Column(db.String(100), nullable=True)
    ifsc_code = db.Column(db.String(11), nullable=True,
                          comment='11-character IFSC code')
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(15), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ── Relationships ──────────────────────────────────────────────────────────
    loans = db.relationship('Loan', backref='bank', lazy='dynamic')

    def to_dict(self) -> dict:
        """Serialize bank profile to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'bank_name': self.bank_name,
            'branch_name': self.branch_name,
            'ifsc_code': self.ifsc_code,
            'address': self.address,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f'<BankProfile user_id={self.user_id} bank={self.bank_name}>'
