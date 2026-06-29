"""
Smart Agro - Database Seeder Script
Run this to populate the database with demo data (proper password hashes).

Usage:
    cd d:/smart_agro/backend
    python seed_data.py
"""

import sys
import os

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db
from app.models.user import User
from app.models.farmer import FarmerProfile
from app.models.expert import ExpertProfile
from app.models.bank import BankProfile
from app.models.crop import Crop
from app.models.crop_price import CropPrice
from app.models.loan import Loan
from app.models.complaint import Complaint
from app.models.notification import Notification
from app.models.query import Query
from datetime import datetime, date, timedelta
import json

app = create_app()

def seed_database():
    with app.app_context():
        print("🌱 Starting Smart Agro Database Seeding...")

        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print("✅ Tables created successfully")

        # ── Users ──────────────────────────────────────────────
        admin = User(name='Admin User', email='admin@smartagro.com', role='admin')
        admin.set_password('Password@123')

        farmer_user = User(name='Rajesh Kumar', email='farmer@smartagro.com', role='farmer')
        farmer_user.set_password('Password@123')

        farmer_user2 = User(name='Sunita Devi', email='farmer2@smartagro.com', role='farmer')
        farmer_user2.set_password('Password@123')

        farmer_user3 = User(name='Mohan Lal', email='farmer3@smartagro.com', role='farmer')
        farmer_user3.set_password('Password@123')

        expert_user = User(name='Dr. Priya Sharma', email='expert@smartagro.com', role='expert')
        expert_user.set_password('Password@123')

        expert_user2 = User(name='Prof. Anil Verma', email='expert2@smartagro.com', role='expert')
        expert_user2.set_password('Password@123')

        bank_user = User(name='Vikram Mehta', email='bank@smartagro.com', role='bank')
        bank_user.set_password('Password@123')

        db.session.add_all([admin, farmer_user, farmer_user2, farmer_user3, expert_user, expert_user2, bank_user])
        db.session.commit()
        print("✅ Users seeded")

        # ── Farmer Profiles ────────────────────────────────────
        farmer1 = FarmerProfile(
            user_id=farmer_user.id,
            farm_name='Kumar Farms',
            farm_location='Ludhiana, Punjab',
            farm_size=12.5,
            soil_type='Loamy',
            phone='9876543210',
            address='Village Raikot, Ludhiana, Punjab - 141109'
        )
        farmer2 = FarmerProfile(
            user_id=farmer_user2.id,
            farm_name='Devi Agriculture',
            farm_location='Nashik, Maharashtra',
            farm_size=8.0,
            soil_type='Sandy Loam',
            phone='9765432109',
            address='Village Igatpuri, Nashik, Maharashtra - 422403'
        )
        farmer3 = FarmerProfile(
            user_id=farmer_user3.id,
            farm_name='Lal Fields',
            farm_location='Jaipur, Rajasthan',
            farm_size=20.0,
            soil_type='Sandy',
            phone='9654321098',
            address='Village Sanganer, Jaipur, Rajasthan - 302029'
        )
        db.session.add_all([farmer1, farmer2, farmer3])
        db.session.commit()
        print("✅ Farmer profiles seeded")

        # ── Expert Profiles ────────────────────────────────────
        expert1 = ExpertProfile(
            user_id=expert_user.id,
            specialization='Crop Disease Management',
            qualification='Ph.D. in Plant Pathology, IARI',
            experience_years=12,
            bio='Expert in identifying and treating crop diseases with 12+ years of field experience.',
            phone='9543210987',
            is_available=True
        )
        expert2 = ExpertProfile(
            user_id=expert_user2.id,
            specialization='Soil Science & Fertilizers',
            qualification='M.Sc. Agriculture, Punjab Agricultural University',
            experience_years=8,
            bio='Soil health and fertilizer management specialist with experience across multiple states.',
            phone='9432109876',
            is_available=True
        )
        db.session.add_all([expert1, expert2])
        db.session.commit()
        print("✅ Expert profiles seeded")

        # ── Bank Profile ───────────────────────────────────────
        bank1 = BankProfile(
            user_id=bank_user.id,
            bank_name='State Bank of India',
            branch_name='Agricultural Finance Branch',
            ifsc_code='SBIN0001234',
            address='Main Road, Ludhiana, Punjab',
            phone='9321098765'
        )
        db.session.add(bank1)
        db.session.commit()
        print("✅ Bank profile seeded")

        # ── Crops ──────────────────────────────────────────────
        crops = [
            Crop(farmer_id=farmer1.id, name='Wheat', variety='HD-2967', area_acres=5.0,
                 planting_date=date(2024, 11, 1), expected_harvest_date=date(2025, 4, 15), status='growing',
                 description='Winter wheat crop, good germination'),
            Crop(farmer_id=farmer1.id, name='Rice', variety='Basmati 1121', area_acres=4.0,
                 planting_date=date(2024, 6, 15), expected_harvest_date=date(2024, 10, 20), status='harvested',
                 description='Kharif season rice, excellent yield'),
            Crop(farmer_id=farmer1.id, name='Cotton', variety='BT Cotton', area_acres=3.5,
                 planting_date=date(2024, 5, 1), expected_harvest_date=date(2024, 11, 30), status='growing',
                 description='Bt cotton, pest-resistant variety'),
            Crop(farmer_id=farmer2.id, name='Tomato', variety='Hybrid', area_acres=2.0,
                 planting_date=date(2024, 9, 1), expected_harvest_date=date(2024, 12, 15), status='growing',
                 description='Hybrid tomato for market'),
            Crop(farmer_id=farmer2.id, name='Onion', variety='Red Onion', area_acres=3.0,
                 planting_date=date(2024, 10, 1), expected_harvest_date=date(2025, 2, 28), status='growing',
                 description='Rabi season onion crop'),
            Crop(farmer_id=farmer3.id, name='Mustard', variety='Pusa Bold', area_acres=8.0,
                 planting_date=date(2024, 10, 15), expected_harvest_date=date(2025, 3, 10), status='growing',
                 description='Main income crop'),
        ]
        db.session.add_all(crops)
        db.session.commit()
        print("✅ Crops seeded")

        # ── Crop Prices ────────────────────────────────────────
        crop_prices_data = [
            ('Rice', 'Basmati', 45.50, 'Azadpur Mandi', 'Delhi'),
            ('Rice', 'Sona Masuri', 38.00, 'Kurnool Market', 'Andhra Pradesh'),
            ('Wheat', 'Sharbati', 28.00, 'Khanna Mandi', 'Punjab'),
            ('Wheat', 'HD-2967', 25.50, 'Karnal Mandi', 'Haryana'),
            ('Corn', 'Yellow Corn', 18.00, 'Davangere Market', 'Karnataka'),
            ('Cotton', 'BT Cotton', 62.00, 'Yavatmal Mandi', 'Maharashtra'),
            ('Sugarcane', 'Co-86032', 3.50, 'Kolhapur Market', 'Maharashtra'),
            ('Tomato', 'Hybrid', 15.00, 'Nashik Mandi', 'Maharashtra'),
            ('Onion', 'Red Onion', 22.00, 'Lasalgaon Mandi', 'Maharashtra'),
            ('Potato', 'Kufri Jyoti', 12.00, 'Agra Mandi', 'Uttar Pradesh'),
            ('Soybean', 'JS-335', 44.00, 'Indore Mandi', 'Madhya Pradesh'),
            ('Groundnut', 'TMV-2', 55.00, 'Gondal Mandi', 'Gujarat'),
            ('Mustard', 'Pusa Bold', 52.00, 'Bharatpur Mandi', 'Rajasthan'),
            ('Turmeric', 'Salem', 115.00, 'Erode Market', 'Tamil Nadu'),
            ('Chilli', 'Guntur', 95.00, 'Guntur Mandi', 'Andhra Pradesh'),
        ]
        for name, variety, price, market, state in crop_prices_data:
            cp = CropPrice(crop_name=name, variety=variety, price_per_kg=price,
                          market_name=market, state=state, updated_by=admin.id)
            db.session.add(cp)
        db.session.commit()
        print("✅ Crop prices seeded")

        # ── Loans ──────────────────────────────────────────────
        loan1 = Loan(
            loan_reference='LOAN-2024-001',
            farmer_id=farmer1.id,
            bank_id=bank1.id,
            amount=250000.00,
            purpose='Equipment',
            description='Need a tractor for farm operations',
            status='approved',
            interest_rate=7.5,
            tenure_months=36,
            reviewed_at=datetime.utcnow(),
            remarks='Approved after document verification. Good credit history.'
        )
        loan2 = Loan(
            loan_reference='LOAN-2024-002',
            farmer_id=farmer2.id,
            amount=100000.00,
            purpose='Seeds',
            description='Need funds for hybrid tomato seeds and fertilizers',
            status='pending'
        )
        loan3 = Loan(
            loan_reference='LOAN-2024-003',
            farmer_id=farmer3.id,
            bank_id=bank1.id,
            amount=500000.00,
            purpose='Irrigation',
            description='Drip irrigation system installation',
            status='rejected',
            reviewed_at=datetime.utcnow(),
            remarks='Insufficient collateral documentation provided.'
        )
        db.session.add_all([loan1, loan2, loan3])
        db.session.commit()
        print("✅ Loans seeded")

        # ── Complaints ─────────────────────────────────────────
        comp1 = Complaint(
            farmer_id=farmer1.id,
            subject='Pest attack on wheat crop',
            description='My wheat crop is under heavy aphid attack near the borders. Need immediate assistance.',
            category='pest',
            status='in_progress',
            priority='high',
            admin_reply='Our expert team has been notified. They will contact you within 24 hours.'
        )
        comp2 = Complaint(
            farmer_id=farmer2.id,
            subject='Market price dispute for tomatoes',
            description='The local mandi is paying below MSP for my tomatoes. Please intervene.',
            category='market',
            status='open',
            priority='medium'
        )
        db.session.add_all([comp1, comp2])
        db.session.commit()
        print("✅ Complaints seeded")

        # ── Queries ────────────────────────────────────────────
        query1 = Query(
            farmer_id=farmer1.id,
            expert_id=expert1.id,
            subject='Yellow spots on wheat leaves',
            question='I noticed yellow-orange spots on my wheat leaves. The plants look weak. Is this rust disease? What should I do?',
            answer='Based on your description, this appears to be Yellow Rust (Stripe Rust) caused by Puccinia striiformis. Immediately apply Propiconazole 25% EC at 0.1% concentration. Spray in the morning. Repeat after 15 days if infection persists. Also ensure good air circulation and avoid excessive nitrogen.',
            status='answered',
            category='disease',
            answered_at=datetime.utcnow() - timedelta(days=2)
        )
        query2 = Query(
            farmer_id=farmer2.id,
            subject='Best fertilizer for tomato in sandy loam soil',
            question='What is the recommended fertilizer schedule for hybrid tomato in sandy loam soil? My current yield is low.',
            status='open',
            category='fertilizer'
        )
        db.session.add_all([query1, query2])
        db.session.commit()
        print("✅ Queries seeded")

        # ── Notifications ──────────────────────────────────────
        notifs = [
            Notification(user_id=farmer_user.id, title='Welcome to Smart Agro!',
                        message='Your farmer account has been created successfully. Explore AI tools and crop management features.',
                        type='success'),
            Notification(user_id=farmer_user.id, title='Loan Approved',
                        message='Your loan application LOAN-2024-001 for ₹2,50,000 has been approved by SBI.',
                        type='success', is_read=True),
            Notification(user_id=farmer_user.id, title='Complaint Update',
                        message='Your complaint about pest attack is being reviewed. Expert team will contact you soon.',
                        type='info'),
            Notification(user_id=farmer_user2.id, title='Welcome to Smart Agro!',
                        message='Your farmer account is ready. Start by adding your crops.',
                        type='success'),
            Notification(user_id=expert_user.id, title='New Query Received',
                        message='Farmer Rajesh Kumar has submitted a new query about wheat disease.',
                        type='info', is_read=True),
            Notification(user_id=bank_user.id, title='New Loan Application',
                        message='A new loan application of ₹1,00,000 from Sunita Devi is pending review.',
                        type='info'),
        ]
        db.session.add_all(notifs)
        db.session.commit()
        print("✅ Notifications seeded")

        print("\n🎉 Database seeding completed successfully!")
        print("\n📋 Demo Credentials (all passwords: Password@123):")
        print("   Admin:   admin@smartagro.com")
        print("   Farmer:  farmer@smartagro.com")
        print("   Expert:  expert@smartagro.com")
        print("   Bank:    bank@smartagro.com")

if __name__ == '__main__':
    seed_database()
