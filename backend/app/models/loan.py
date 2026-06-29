"""
Smart Agro - Loan Model
========================
Tracks loan applications by farmers to banks.
Lifecycle: pending → approved/rejected → disbursed
"""

import json
from datetime import datetime
from app import db


class Loan(db.Model):
    """
    Represents a loan application submitted by a farmer.
    Managed by bank officers who can approve, reject, or disburse loans.
    """
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys
    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey('farmer_profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    bank_id = db.Column(
        db.Integer,
        db.ForeignKey('bank_profiles.id', ondelete='SET NULL'),
        nullable=True,
        index=True,
        comment='Bank that reviewed this loan (null until assigned)'
    )

    # Loan details
    amount = db.Column(db.Numeric(12, 2), nullable=False, comment='Loan amount in INR')
    purpose = db.Column(db.String(200), nullable=False,
                        comment='Short purpose (e.g., Crop Input, Equipment Purchase)')
    description = db.Column(db.Text, nullable=True,
                            comment='Detailed description of loan purpose')

    # Loan terms (set by bank upon approval)
    interest_rate = db.Column(db.Float, nullable=True, comment='Annual interest rate in %')
    tenure_months = db.Column(db.Integer, nullable=True, comment='Loan tenure in months')

    # Status tracking
    status = db.Column(
        db.Enum('pending', 'approved', 'rejected', 'disbursed', name='loan_status'),
        default='pending',
        nullable=False,
        index=True
    )

    # Remarks from bank officer
    remarks = db.Column(db.Text, nullable=True)

    # Supporting documents (stored as JSON array of filenames)
    documents = db.Column(db.Text, nullable=True, comment='JSON array of document filenames')

    # Reference number for tracking
    reference_number = db.Column(db.String(20), unique=True, nullable=True, index=True)

    # Timestamps
    applied_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    # ── Document helpers ───────────────────────────────────────────────────────
    def get_documents(self) -> list:
        """Parse the JSON documents field into a Python list."""
        if self.documents:
            try:
                return json.loads(self.documents)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def set_documents(self, docs: list) -> None:
        """Serialize a list of document filenames to JSON for storage."""
        self.documents = json.dumps(docs)

    def to_dict(self) -> dict:
        """Serialize loan to dictionary."""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'bank_id': self.bank_id,
            'amount': float(self.amount) if self.amount else None,
            'purpose': self.purpose,
            'description': self.description,
            'interest_rate': self.interest_rate,
            'tenure_months': self.tenure_months,
            'status': self.status,
            'remarks': self.remarks,
            'documents': self.get_documents(),
            'reference_number': self.reference_number,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
        }

    def __repr__(self) -> str:
        return f'<Loan #{self.reference_number} ₹{self.amount} ({self.status})>'
