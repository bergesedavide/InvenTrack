from flask import Blueprint, request, jsonify
from app.services.order_service import OrderService

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/", methods=["GET"])
def get_orders():
    status = request.args.get('status')
    limit = request.args.get('limit', 365, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    order_service = OrderService()
    orders = order_service.get_all_orders(status=status, limit=limit, offset=offset)
    
    return jsonify(orders), 200

@orders_bp.route("/<order_id>", methods=["GET"])
def get_order(order_id):
    order_service = OrderService()
    order = order_service.get_order_by_id(order_id)
    
    if not order:
        return jsonify({"error": "Ordine non trovato"}), 404
    
    return jsonify(order), 200

@orders_bp.route("/stats", methods=["GET"])
def get_order_stats():
    company_id = request.args.get('company_id', type=int)
    
    order_service = OrderService()
    stats = order_service.get_order_stats(company_id)
    
    return jsonify(stats), 200