from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
from app.database.category_repository import CategoryRepository

prod_bp = Blueprint("products", __name__)

def build_product_response(products, catRepo):
        result = []

        for p in products:
            result.append({
                "id": p.get("id"),
                "name": p["name"],
                "idCategory": p["idCategory"],
                "category": catRepo.get_desc_by_id(p["idCategory"]),
                "price": p["price"],
                "stock": p.get("stock", 0)
            })

        return result

@prod_bp.route("/", methods=["GET"])
def get_all_products():
    prodService = ProductService()
    catRepo = CategoryRepository()
    
    # Prendi categoria dalla query string
    category_id = request.args.get('category_id', type=int)
    
    if category_id:
        products = prodService.get_all_product(category_id)
    else:
        products = prodService.get_all_product()
    
    result = build_product_response(products, catRepo)
    return jsonify(result), 200

@prod_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    prodService = ProductService()
    catRepo = CategoryRepository()
    
    product = prodService.get_product_by_id(product_id)
    
    if not product:
        return jsonify({"error": "Prodotto non trovato"}), 404
    
    result = {
        "id": product.get("id"),
        "name": product.get("name"),
        "category": catRepo.get_desc_by_id(product.get("idCategory")),
        "price": product.get("price"),
        "stock": product.get("stock", 0)
    }
    
    return jsonify(result), 200

@prod_bp.route("/<int:product_id>/stock", methods=["PATCH"])
def update_stock(product_id):
    data = request.get_json()
    new_stock = data.get('stock')
    
    if new_stock is None:
        return jsonify({"error": "Stock non specificato"}), 400
    
    try:
        from app.database.product_repository import ProductRepository
        repo = ProductRepository()
        
        # Aggiorna stock
        result = repo.db.table(repo.tblAlias).update({"stock": new_stock}).eq("id", product_id).execute()
        
        return jsonify({"message": "Stock aggiornato", "stock": new_stock}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500