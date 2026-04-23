from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
from app.database.category_repository import CategoryRepository

prod_bp = Blueprint("products", __name__)

def build_product_response(products, catRepo):
        result = []

        for p in products:
            result.append({
                "name": p["name"],
                "idCategory": p["idCategory"],
                "category": catRepo.get_desc_by_id(p["idCategory"]),
                "price": p["price"]
            })

        return result

@prod_bp.route("/", methods=["GET"])
def get_all_products():
    prodService = ProductService()
    catRepo = CategoryRepository()

    products = prodService.get_all_product(9)

    result = build_product_response(products, catRepo)

    print(result)
    return jsonify(result), 200

@prod_bp.route("/subscription", methods=["GET"])
def get_all_products_subs():
    prodService = ProductService()
    catRepo = CategoryRepository()

    products = prodService.get_all_product_by_id(9)

    result = build_product_response(products, catRepo)

    return jsonify(result), 200