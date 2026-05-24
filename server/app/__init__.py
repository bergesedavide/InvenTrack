import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS

from app.routes.authentications import auth_bp
from app.routes.products import prod_bp
from app.routes.calendars import calendar_bp
from app.routes.ai import ai_bp
from app.routes.orders import orders_bp
from app.routes.analytics import analytics_bp
from app.routes.system import system_bp
from app.routes.simulation import simulation_bp

app = Flask(__name__)
CORS(app, origins=["https://wcwffjp7-5173.euw.devtunnels.ms", "http://localhost:5173"])

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(prod_bp, url_prefix="/products")
app.register_blueprint(calendar_bp, url_prefix="/calendars")
app.register_blueprint(ai_bp, url_prefix="/ai")
app.register_blueprint(orders_bp, url_prefix="/orders")
app.register_blueprint(analytics_bp, url_prefix="/analytics")
app.register_blueprint(system_bp, url_prefix="/system")
app.register_blueprint(simulation_bp, url_prefix="/simulation")

@app.route('/')
def root():
    return jsonify({"message": "InvenTrack API", "status": "online"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# Avvia scheduler calendario
from app.services.calendar_scheduler import CalendarScheduler
scheduler = CalendarScheduler(interval_minutes=5)
scheduler.start()

from app.services.simulation_service import SimulationService
simulation = SimulationService()
simulation.start_simulation()

import atexit
atexit.register(lambda: scheduler.stop())
atexit.register(lambda: simulation.stop_simulation())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)