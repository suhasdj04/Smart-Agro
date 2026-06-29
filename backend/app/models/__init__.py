"""
Smart Agro - Models Package
=============================
This module imports all models so Flask-Migrate (Alembic) can detect them
and generate correct database migration scripts.

All models MUST be imported here.
"""

from app.models.user import User
from app.models.farmer import FarmerProfile
from app.models.expert import ExpertProfile
from app.models.bank import BankProfile
from app.models.crop import Crop
from app.models.crop_price import CropPrice
from app.models.loan import Loan
from app.models.complaint import Complaint
from app.models.notification import Notification
from app.models.disease_prediction import DiseasePrediction
from app.models.recommendation import Recommendation
from app.models.query import Query

__all__ = [
    'User',
    'FarmerProfile',
    'ExpertProfile',
    'BankProfile',
    'Crop',
    'CropPrice',
    'Loan',
    'Complaint',
    'Notification',
    'DiseasePrediction',
    'Recommendation',
    'Query',
]
