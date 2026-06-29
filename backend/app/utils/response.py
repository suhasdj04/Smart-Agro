"""Utility response helpers for consistent API responses."""
from flask import jsonify


def success_response(data=None, message='Success', status_code=200):
    """Return a standardized success JSON response."""
    response = {
        'success': True,
        'message': message,
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def error_response(message='An error occurred', status_code=400, errors=None):
    """Return a standardized error JSON response."""
    response = {
        'success': False,
        'message': message,
    }
    if errors is not None:
        response['errors'] = errors
    return jsonify(response), status_code


def paginated_response(items, total, page, per_page, message='Success'):
    """Return a paginated JSON response."""
    return jsonify({
        'success': True,
        'message': message,
        'data': items,
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1,
        }
    }), 200
