from flask import Flask
from flask_cors import CORS

from app.services.calendar_scheduler import CalendarScheduler

scheduler = CalendarScheduler(interval_minutes=1)

def create_app():
    app = Flask(__name__)
    CORS(app)

    # config base
    app.config["JSON_SORT_KEYS"] = False

    # import blueprint
    from app.routes.calendars import calendar_bp
    from app.routes.authentications import auth_bp

    app.register_blueprint(calendar_bp, url_prefix="/calendars")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
