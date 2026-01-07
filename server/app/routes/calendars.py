from flask import Blueprint, jsonify
from app.services.calendar_service import CalendarService
from app.services.calendar_scheduler import CalendarScheduler

calendar_bp = Blueprint("calendars", __name__)
calendar_service = CalendarService()
calendar_scheduler = CalendarScheduler(1)

# Ritorno della data in formato "dd-mm-yyyy"
@calendar_bp.route("/", methods=["GET"])
def get_date():
    date = calendar_service.get_date()
    return jsonify({"date": date}), 200

@calendar_bp.route("/full", methods=["GET"])
def get_full_date():
    date = calendar_service.get_full_date()
    return jsonify({"date": date}), 200

@calendar_bp.route("/advance", methods=["GET", "POST"])
def advance_calendar():
    result = calendar_service.advance_calendar()
    return jsonify(result), 200

@calendar_bp.route("/can-ship", methods=["GET"])
def can_ship():
    result = calendar_service.can_ship()
    return jsonify({"ship": result}), 200

@calendar_bp.route("/start", methods=["GET", "POST"])
def start():
    calendar_scheduler.start()
    return jsonify({"message": "Avanzamento automatico della data iniziato"}), 200

@calendar_bp.route("/stop", methods=["GET", "POST"])
def stop():
    calendar_scheduler.stop()
    return jsonify({"message": "Avanzamento automatico della data fermato"}), 200