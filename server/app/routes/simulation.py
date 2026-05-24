from flask import Blueprint, request, jsonify
from app.services.simulation_service import SimulationService
from app.core.decorators import token_required

simulation_bp = Blueprint("simulation", __name__)
simulation_service = SimulationService()

@simulation_bp.route("/start", methods=["POST"])
#@token_required
def start_simulation():
    """Avvia la simulazione automatica"""
    result = simulation_service.start_simulation()
    if result:
        return jsonify({"message": "Simulazione avviata", "status": "running"}), 200
    else:
        return jsonify({"message": "Simulazione già in esecuzione", "status": "already_running"}), 400

@simulation_bp.route("/stop", methods=["POST"])
#@token_required
def stop_simulation():
    """Ferma la simulazione automatica"""
    result = simulation_service.stop_simulation()
    if result:
        return jsonify({"message": "Simulazione fermata", "status": "stopped"}), 200
    else:
        return jsonify({"message": "Simulazione non in esecuzione", "status": "not_running"}), 400

@simulation_bp.route("/status", methods=["GET"])
def get_simulation_status():
    """Restituisce lo stato corrente della simulazione"""
    stats = simulation_service.get_simulation_stats()
    return jsonify(stats), 200

@simulation_bp.route("/reset", methods=["POST"])
def reset_simulation():
    """Resetta completamente la simulazione"""
    result = simulation_service.reset_simulation()
    return jsonify(result), 200

@simulation_bp.route("/generate-orders", methods=["POST"])
def generate_orders():
    """Genera un lotto di ordini manualmente"""
    data = request.get_json() or {}
    max_orders = data.get("max_orders", 10)
    
    orders = simulation_service._generate_random_orders(max_orders)
    return jsonify({"message": f"Generati {orders} ordini", "orders_generated": orders}), 200

@simulation_bp.route("/generate-clients", methods=["POST"])
def generate_clients():
    """Genera clienti casuali manualmente"""
    data = request.get_json() or {}
    max_clients = data.get("max_clients", 5)
    
    clients = simulation_service._generate_random_clients(max_clients)
    return jsonify({"message": f"Generati {clients} clienti", "clients_generated": clients}), 200

@simulation_bp.route("/auto-restock", methods=["POST"])
def auto_restock():
    """Esegue rifornimento automatico manualmente"""
    restocks = simulation_service._auto_restock()
    return jsonify({"message": f"Eseguiti {restocks} rifornimenti", "restocks": restocks}), 200