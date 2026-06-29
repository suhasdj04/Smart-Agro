"""Expert routes blueprint."""
from flask import Blueprint, request
from app.middleware.role_middleware import expert_required
from app.controllers.expert_controller import (
    get_expert_profile, update_expert_profile,
    get_all_queries, get_single_query, answer_query,
    get_all_farmers, get_farmer_by_id, get_expert_dashboard_stats
)

expert_bp = Blueprint('expert', __name__)


@expert_bp.route('/profile', methods=['GET'])
@expert_required
def profile(current_user):
    return get_expert_profile(current_user)


@expert_bp.route('/profile', methods=['PUT'])
@expert_required
def update_profile(current_user):
    return update_expert_profile(current_user, request.get_json())


@expert_bp.route('/queries', methods=['GET'])
@expert_required
def queries(current_user):
    return get_all_queries(request.args)


@expert_bp.route('/queries/<int:query_id>', methods=['GET'])
@expert_required
def single_query(current_user, query_id):
    return get_single_query(query_id)


@expert_bp.route('/queries/<int:query_id>/answer', methods=['PUT'])
@expert_required
def answer_query_route(current_user, query_id):
    return answer_query(current_user, query_id, request.get_json())


@expert_bp.route('/farmers', methods=['GET'])
@expert_required
def farmers(current_user):
    return get_all_farmers(request.args)


@expert_bp.route('/farmers/<int:farmer_id>', methods=['GET'])
@expert_required
def farmer_detail(current_user, farmer_id):
    return get_farmer_by_id(farmer_id)


@expert_bp.route('/dashboard-stats', methods=['GET'])
@expert_required
def dashboard(current_user):
    return get_expert_dashboard_stats(current_user)
