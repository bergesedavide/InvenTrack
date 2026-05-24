from flask import Blueprint, jsonify, request
from app.services.system_service import SystemService

system_bp = Blueprint("system", __name__)

@system_bp.route("/status", methods=["GET"])
def get_system_status():
    system = SystemService()
    
    return jsonify({
        "database": system.check_database(),
        "api": "online",
        "aiEngine": system.check_ai_engine(),
        "websocket": "online",
        "lastBackup": system.get_last_backup_date(),
        "uptime": system.get_uptime(),
        "responseTime": system.get_avg_response_time(),
        "activeUsers": system.get_active_users(),
        "totalRequests": system.get_total_requests()
    }), 200

@system_bp.route("/changelog", methods=["GET"])
def get_changelog():
    limit = request.args.get('limit', 10, type=int)
    
    system = SystemService()
    changelog = system.get_changelog(limit)
    
    return jsonify(changelog), 200