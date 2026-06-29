"""Farmer routes blueprint."""
from flask import Blueprint, request
from app.middleware.role_middleware import farmer_required
from app.controllers.farmer_controller import (
    get_farmer_profile, update_farmer_profile, upload_profile_image,
    get_crops, create_crop, get_crop, update_crop, delete_crop, upload_crop_image,
    get_loans, apply_for_loan, get_loan,
    get_complaints, raise_complaint, get_complaint,
    get_queries, submit_query, get_query,
    get_crop_prices_farmer, get_dashboard_stats
)

farmer_bp = Blueprint('farmer', __name__)


# ── Profile ─────────────────────────────────────────────────
@farmer_bp.route('/profile', methods=['GET'])
@farmer_required
def profile(current_user):
    return get_farmer_profile(current_user)


@farmer_bp.route('/profile', methods=['PUT'])
@farmer_required
def update_profile(current_user):
    return update_farmer_profile(current_user, request.get_json())


@farmer_bp.route('/profile/image', methods=['POST'])
@farmer_required
def profile_image(current_user):
    return upload_profile_image(current_user, request.files.get('image'))


# ── Crops ────────────────────────────────────────────────────
@farmer_bp.route('/crops', methods=['GET'])
@farmer_required
def crops(current_user):
    return get_crops(current_user, request.args)


@farmer_bp.route('/crops', methods=['POST'])
@farmer_required
def add_crop(current_user):
    return create_crop(current_user, request.get_json())


@farmer_bp.route('/crops/<int:crop_id>', methods=['GET'])
@farmer_required
def single_crop(current_user, crop_id):
    return get_crop(current_user, crop_id)


@farmer_bp.route('/crops/<int:crop_id>', methods=['PUT'])
@farmer_required
def update_crop_route(current_user, crop_id):
    return update_crop(current_user, crop_id, request.get_json())


@farmer_bp.route('/crops/<int:crop_id>', methods=['DELETE'])
@farmer_required
def delete_crop_route(current_user, crop_id):
    return delete_crop(current_user, crop_id)


@farmer_bp.route('/crops/<int:crop_id>/image', methods=['POST'])
@farmer_required
def crop_image(current_user, crop_id):
    return upload_crop_image(current_user, crop_id, request.files.get('image'))


# ── Loans ─────────────────────────────────────────────────────
@farmer_bp.route('/loans', methods=['GET'])
@farmer_required
def loans(current_user):
    return get_loans(current_user)


@farmer_bp.route('/loans', methods=['POST'])
@farmer_required
def apply_loan(current_user):
    return apply_for_loan(current_user, request.get_json())


@farmer_bp.route('/loans/<int:loan_id>', methods=['GET'])
@farmer_required
def single_loan(current_user, loan_id):
    return get_loan(current_user, loan_id)


# ── Complaints ────────────────────────────────────────────────
@farmer_bp.route('/complaints', methods=['GET'])
@farmer_required
def complaints(current_user):
    return get_complaints(current_user)


@farmer_bp.route('/complaints', methods=['POST'])
@farmer_required
def raise_complaint_route(current_user):
    return raise_complaint(current_user, request.get_json())


@farmer_bp.route('/complaints/<int:complaint_id>', methods=['GET'])
@farmer_required
def single_complaint(current_user, complaint_id):
    return get_complaint(current_user, complaint_id)


# ── Queries ───────────────────────────────────────────────────
@farmer_bp.route('/queries', methods=['GET'])
@farmer_required
def queries(current_user):
    return get_queries(current_user)


@farmer_bp.route('/queries', methods=['POST'])
@farmer_required
def submit_query_route(current_user):
    return submit_query(current_user, request.get_json())


@farmer_bp.route('/queries/<int:query_id>', methods=['GET'])
@farmer_required
def single_query(current_user, query_id):
    return get_query(current_user, query_id)


# ── Crop Prices ───────────────────────────────────────────────
@farmer_bp.route('/crop-prices', methods=['GET'])
@farmer_required
def crop_prices(current_user):
    return get_crop_prices_farmer(request.args)


# ── Dashboard ─────────────────────────────────────────────────
@farmer_bp.route('/dashboard-stats', methods=['GET'])
@farmer_required
def dashboard(current_user):
    return get_dashboard_stats(current_user)
