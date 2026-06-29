"""Farmer controller - business logic for all farmer operations."""
from datetime import datetime
from app import db
from app.models.farmer import FarmerProfile
from app.models.crop import Crop
from app.models.crop_price import CropPrice
from app.models.loan import Loan
from app.models.complaint import Complaint
from app.models.notification import Notification
from app.models.query import Query
from app.utils.response import success_response, error_response
from app.utils.helpers import generate_loan_reference
from app.services.file_service import save_file
from app.services.notification_service import (
    notify_loan_applied, notify_new_loan_to_bank
)
from app.models.bank import BankProfile
from app.models.user import User


# ── Profile ──────────────────────────────────────────────────

def get_farmer_profile(current_user):
    """Get farmer profile."""
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)
    data = current_user.to_dict()
    data['profile'] = profile.to_dict()
    return success_response(data=data)


def update_farmer_profile(current_user, data):
    """Update farmer profile."""
    if not data:
        return error_response('Request body required.')
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)
    try:
        # Update user name
        if 'name' in data:
            current_user.name = data['name'].strip()
        # Update profile fields
        updatable = ['farm_name', 'farm_location', 'farm_size', 'soil_type', 'phone', 'aadhaar', 'address']
        for field in updatable:
            if field in data:
                setattr(profile, field, data[field])
        db.session.commit()
        return success_response(data=profile.to_dict(), message='Profile updated successfully.')
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


def upload_profile_image(current_user, image_file):
    """Upload farmer profile image."""
    if not image_file:
        return error_response('No image file provided.')
    try:
        _, url_path = save_file(image_file, 'profiles')
        profile = current_user.farmer_profile
        profile.profile_image = url_path
        db.session.commit()
        return success_response(data={'image_url': url_path}, message='Profile image updated.')
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


# ── Crops ────────────────────────────────────────────────────

def get_crops(current_user, args):
    """List farmer's crops with optional filters."""
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)

    query = Crop.query.filter_by(farmer_id=profile.id)

    # Filter by status
    status = args.get('status')
    if status:
        query = query.filter(Crop.status == status)

    # Search by name
    search = args.get('search')
    if search:
        query = query.filter(Crop.name.ilike(f'%{search}%'))

    crops = query.order_by(Crop.created_at.desc()).all()
    return success_response(data=[c.to_dict() for c in crops])


def create_crop(current_user, data):
    """Create a new crop record."""
    if not data:
        return error_response('Request body required.')
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)

    name = data.get('name', '').strip()
    if not name:
        return error_response('Crop name is required.')

    try:
        planting_date = None
        if data.get('planting_date'):
            planting_date = datetime.strptime(data['planting_date'], '%Y-%m-%d').date()
        expected_harvest = None
        if data.get('expected_harvest_date'):
            expected_harvest = datetime.strptime(data['expected_harvest_date'], '%Y-%m-%d').date()

        crop = Crop(
            farmer_id=profile.id,
            name=name,
            variety=data.get('variety', ''),
            area_acres=data.get('area_acres'),
            planting_date=planting_date,
            expected_harvest_date=expected_harvest,
            status=data.get('status', 'growing'),
            description=data.get('description', '')
        )
        db.session.add(crop)
        db.session.commit()
        return success_response(data=crop.to_dict(), message='Crop added successfully.', status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


def get_crop(current_user, crop_id):
    """Get a single crop by ID."""
    profile = current_user.farmer_profile
    crop = Crop.query.filter_by(id=crop_id, farmer_id=profile.id).first()
    if not crop:
        return error_response('Crop not found.', 404)
    return success_response(data=crop.to_dict())


def update_crop(current_user, crop_id, data):
    """Update a crop record."""
    if not data:
        return error_response('Request body required.')
    profile = current_user.farmer_profile
    crop = Crop.query.filter_by(id=crop_id, farmer_id=profile.id).first()
    if not crop:
        return error_response('Crop not found.', 404)

    try:
        updatable = ['name', 'variety', 'area_acres', 'status', 'description']
        for field in updatable:
            if field in data:
                setattr(crop, field, data[field])
        if data.get('planting_date'):
            crop.planting_date = datetime.strptime(data['planting_date'], '%Y-%m-%d').date()
        if data.get('expected_harvest_date'):
            crop.expected_harvest_date = datetime.strptime(data['expected_harvest_date'], '%Y-%m-%d').date()
        if data.get('actual_harvest_date'):
            crop.actual_harvest_date = datetime.strptime(data['actual_harvest_date'], '%Y-%m-%d').date()
        db.session.commit()
        return success_response(data=crop.to_dict(), message='Crop updated successfully.')
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


def delete_crop(current_user, crop_id):
    """Delete a crop record."""
    profile = current_user.farmer_profile
    crop = Crop.query.filter_by(id=crop_id, farmer_id=profile.id).first()
    if not crop:
        return error_response('Crop not found.', 404)
    try:
        db.session.delete(crop)
        db.session.commit()
        return success_response(message='Crop deleted successfully.')
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


def upload_crop_image(current_user, crop_id, image_file):
    """Upload a crop image."""
    profile = current_user.farmer_profile
    crop = Crop.query.filter_by(id=crop_id, farmer_id=profile.id).first()
    if not crop:
        return error_response('Crop not found.', 404)
    if not image_file:
        return error_response('No image provided.')
    try:
        _, url_path = save_file(image_file, 'crops')
        crop.image_url = url_path
        db.session.commit()
        return success_response(data={'image_url': url_path}, message='Crop image uploaded.')
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


# ── Loans ─────────────────────────────────────────────────────

def get_loans(current_user):
    """List farmer's loan applications."""
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)
    loans = Loan.query.filter_by(farmer_id=profile.id).order_by(Loan.applied_at.desc()).all()
    return success_response(data=[l.to_dict() for l in loans])


def apply_for_loan(current_user, data):
    """Apply for an agricultural loan."""
    if not data:
        return error_response('Request body required.')
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)

    amount = data.get('amount')
    purpose = data.get('purpose')
    if not amount or not purpose:
        return error_response('Amount and purpose are required.')

    try:
        loan = Loan(
            loan_reference=generate_loan_reference(),
            farmer_id=profile.id,
            amount=float(amount),
            purpose=purpose,
            description=data.get('description', ''),
            tenure_months=data.get('tenure_months'),
            status='pending'
        )
        db.session.add(loan)
        db.session.commit()

        # Notify farmer
        notify_loan_applied(current_user.id, float(amount))

        # Notify all bank officers
        bank_users = User.query.filter_by(role='bank', is_active=True).all()
        for bu in bank_users:
            notify_new_loan_to_bank(bu.id, current_user.name, float(amount))

        return success_response(data=loan.to_dict(), message='Loan application submitted successfully.', status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


def get_loan(current_user, loan_id):
    """Get a single loan application."""
    profile = current_user.farmer_profile
    loan = Loan.query.filter_by(id=loan_id, farmer_id=profile.id).first()
    if not loan:
        return error_response('Loan not found.', 404)
    return success_response(data=loan.to_dict())


# ── Complaints ────────────────────────────────────────────────

def get_complaints(current_user):
    """List farmer's complaints."""
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)
    complaints = Complaint.query.filter_by(farmer_id=profile.id).order_by(Complaint.created_at.desc()).all()
    return success_response(data=[c.to_dict() for c in complaints])


def raise_complaint(current_user, data):
    """Raise a new complaint."""
    if not data:
        return error_response('Request body required.')
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)

    subject = data.get('subject', '').strip()
    description = data.get('description', '').strip()
    if not subject or not description:
        return error_response('Subject and description are required.')

    try:
        complaint = Complaint(
            farmer_id=profile.id,
            subject=subject,
            description=description,
            category=data.get('category', 'other'),
            priority=data.get('priority', 'medium')
        )
        db.session.add(complaint)
        db.session.commit()
        return success_response(data=complaint.to_dict(), message='Complaint submitted successfully.', status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


def get_complaint(current_user, complaint_id):
    """Get a single complaint."""
    profile = current_user.farmer_profile
    complaint = Complaint.query.filter_by(id=complaint_id, farmer_id=profile.id).first()
    if not complaint:
        return error_response('Complaint not found.', 404)
    return success_response(data=complaint.to_dict())


# ── Queries ───────────────────────────────────────────────────

def get_queries(current_user):
    """List farmer's queries."""
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)
    queries = Query.query.filter_by(farmer_id=profile.id).order_by(Query.created_at.desc()).all()
    return success_response(data=[q.to_dict() for q in queries])


def submit_query(current_user, data):
    """Submit a new query to experts."""
    if not data:
        return error_response('Request body required.')
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)

    subject = data.get('subject', '').strip()
    question = data.get('question', '').strip()
    if not subject or not question:
        return error_response('Subject and question are required.')

    try:
        query = Query(
            farmer_id=profile.id,
            subject=subject,
            question=question,
            category=data.get('category', 'general')
        )
        db.session.add(query)
        db.session.commit()

        # Notify available experts
        from app.models.expert import ExpertProfile
        experts = ExpertProfile.query.filter_by(is_available=True).all()
        for exp in experts:
            expert_user = User.query.get(exp.user_id)
            if expert_user:
                from app.services.notification_service import notify_new_query_to_expert
                notify_new_query_to_expert(expert_user.id, current_user.name, subject)

        return success_response(data=query.to_dict(), message='Query submitted successfully.', status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)


def get_query(current_user, query_id):
    """Get a single query with answer."""
    profile = current_user.farmer_profile
    query = Query.query.filter_by(id=query_id, farmer_id=profile.id).first()
    if not query:
        return error_response('Query not found.', 404)
    return success_response(data=query.to_dict())


# ── Crop Prices ───────────────────────────────────────────────

def get_crop_prices_farmer(args):
    """View current crop prices."""
    query = CropPrice.query
    crop_name = args.get('crop_name')
    if crop_name:
        query = query.filter(CropPrice.crop_name.ilike(f'%{crop_name}%'))
    prices = query.order_by(CropPrice.date.desc(), CropPrice.crop_name).all()
    return success_response(data=[p.to_dict() for p in prices])


# ── Dashboard ─────────────────────────────────────────────────

def get_dashboard_stats(current_user):
    """Get farmer dashboard statistics."""
    profile = current_user.farmer_profile
    if not profile:
        return error_response('Farmer profile not found.', 404)

    total_crops = Crop.query.filter_by(farmer_id=profile.id).count()
    growing_crops = Crop.query.filter_by(farmer_id=profile.id, status='growing').count()
    total_loans = Loan.query.filter_by(farmer_id=profile.id).count()
    active_loans = Loan.query.filter_by(farmer_id=profile.id, status='approved').count()
    pending_loans = Loan.query.filter_by(farmer_id=profile.id, status='pending').count()
    open_complaints = Complaint.query.filter_by(farmer_id=profile.id, status='open').count()
    unread_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    pending_queries = Query.query.filter_by(farmer_id=profile.id, status='open').count()

    # Recent crops
    recent_crops = Crop.query.filter_by(farmer_id=profile.id).order_by(Crop.created_at.desc()).limit(5).all()

    # Loan status distribution
    loan_status = {}
    for status in ['pending', 'approved', 'rejected', 'disbursed']:
        loan_status[status] = Loan.query.filter_by(farmer_id=profile.id, status=status).count()

    return success_response(data={
        'total_crops': total_crops,
        'growing_crops': growing_crops,
        'total_loans': total_loans,
        'active_loans': active_loans,
        'pending_loans': pending_loans,
        'open_complaints': open_complaints,
        'unread_notifications': unread_notifications,
        'pending_queries': pending_queries,
        'recent_crops': [c.to_dict() for c in recent_crops],
        'loan_status_distribution': loan_status,
    })
