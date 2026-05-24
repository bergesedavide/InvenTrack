from flask import Blueprint, request, jsonify
from app.services.analytics_service import AnalyticsService

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/kpi", methods=["GET"])
def get_kpi():
    company_id = request.args.get('company_id', type=int)
    
    analytics = AnalyticsService()
    kpi = analytics.get_kpi(company_id)
    
    return jsonify(kpi), 200

@analytics_bp.route("/sales", methods=["GET"])
def get_sales():
    period = request.args.get('period', 'year')
    
    analytics = AnalyticsService()
    sales = analytics.get_sales_trend(period)
    
    return jsonify(sales), 200

@analytics_bp.route("/categories", methods=["GET"])
def get_category_sales():
    analytics = AnalyticsService()
    categories = analytics.get_category_distribution()
    
    return jsonify(categories), 200

@analytics_bp.route("/top-products", methods=["GET"])
def get_top_products():
    limit = request.args.get('limit', 5, type=int)
    
    analytics = AnalyticsService()
    products = analytics.get_top_products(limit)
    
    return jsonify(products), 200

@analytics_bp.route("/critical-stock", methods=["GET"])
def get_critical_stock():
    threshold = request.args.get('threshold', 5, type=int)
    
    analytics = AnalyticsService()
    critical = analytics.get_critical_stock(threshold)
    
    return jsonify(critical), 200

@analytics_bp.route("/recent-activities", methods=["GET"])
def get_recent_activities():
    limit = request.args.get('limit', 10, type=int)
    company_id = request.args.get('company_id', type=int)
    
    analytics = AnalyticsService()
    activities = analytics.get_recent_activities(limit, company_id)
    
    return jsonify(activities), 200