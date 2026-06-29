"""
Smart Agro Backend - Flask Application Factory
"""
import os
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__, instance_relative_config=False)

    # ── Load Config ────────────────────────────────────────────
    from app.config.settings import config_by_name
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config_by_name.get(config_name, config_by_name['development']))

    # ── Extensions ────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app,
         resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"]}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # ── Ensure upload directory exists ────────────────────────
    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'crops'), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'profiles'), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, 'disease'), exist_ok=True)

    # ── Import all models (needed for Flask-Migrate) ──────────
    with app.app_context():
        from app.models import (  # noqa: F401
            user, farmer, expert, bank, crop, crop_price,
            loan, complaint, notification, disease_prediction,
            recommendation, query
        )

    # ── Register Blueprints ───────────────────────────────────
    from app.routes.auth import auth_bp
    from app.routes.farmer import farmer_bp
    from app.routes.expert import expert_bp
    from app.routes.bank import bank_bp
    from app.routes.admin import admin_bp
    from app.routes.ai import ai_bp
    from app.routes.weather import weather_bp
    from app.routes.crop_prices import crop_prices_bp
    from app.routes.notifications import notifications_bp

    app.register_blueprint(auth_bp,         url_prefix='/api/auth')
    app.register_blueprint(farmer_bp,       url_prefix='/api/farmer')
    app.register_blueprint(expert_bp,       url_prefix='/api/expert')
    app.register_blueprint(bank_bp,         url_prefix='/api/bank')
    app.register_blueprint(admin_bp,        url_prefix='/api/admin')
    app.register_blueprint(ai_bp,           url_prefix='/api/ai')
    app.register_blueprint(weather_bp,      url_prefix='/api/weather')
    app.register_blueprint(crop_prices_bp,  url_prefix='/api/crop-prices')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')

    # ── Serve uploaded files ───────────────────────────────────
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
        return send_from_directory(upload_folder, filename)

    # ── JWT Error Handlers ────────────────────────────────────
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'success': False, 'message': 'Token has expired. Please login again.'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'success': False, 'message': 'Invalid token. Please login again.'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'success': False, 'message': 'Authorization token is required.'}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({'success': False, 'message': 'Token has been revoked.'}), 401

    # ── Health Check ──────────────────────────────────────────
    @app.route('/api/health')
    def health_check():
        return jsonify({'success': True, 'message': 'Smart Agro API is running', 'version': '1.0.0'})

    # ── Global Error Handlers ─────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'success': False, 'message': 'Resource not found'}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'success': False, 'message': 'Method not allowed'}), 405

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

    return app
