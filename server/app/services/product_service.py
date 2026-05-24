from app.database.product_repository import ProductRepository
from app.database.category_repository import CategoryRepository
from app.database.company_repository import CompanyRepository
from typing import List, Dict, Any, Optional

class ProductService:
    def __init__(self):
        self.prodRepo = ProductRepository()
        self.catRepo = CategoryRepository()
        self.compRepo = CompanyRepository()
    
    def get_all_product(self, idCategory: int = None):
        product = self.prodRepo.get_all_product(idCategory)
        
        if not product:
            return []
        
        for p in product:
            p["name"] = p.pop("nome")
            p["idCategory"] = p.pop("idCategoria")
            p["price"] = p.pop("prezzo")
            p["idCompany"] = p.pop("idAzienda")

        return product
    
    def get_all_product_by_id(self, idCategory: int = None):
        product = self.prodRepo.get_all_product_by_id(idCategory)

        if not product:
            return []
        
        for p in product:
            p["name"] = p.pop("nome")
            p["idCategory"] = p.pop("idCategoria")
            p["price"] = p.pop("prezzo")
            p["idCompany"] = p.pop("idAzienda")
    
        print(product)
        return product
    
    # Aggiungi questi metodi a ProductService

    def get_product_by_id(self, product_id: int) -> Dict[str, Any]:
        """Recupera un singolo prodotto per ID"""
        product = self.prodRepo.get_product_by_id(product_id)
        if product:
            return {
                "id": product.get("id"),
                "name": product.get("nome"),
                "category_id": product.get("idCategoria"),
                "category": self.catRepo.get_desc_by_id(product.get("idCategoria")),
                "price": product.get("prezzo"),
                "stock": product.get("stock", 0),
                "company_id": product.get("idAzienda")
            }
        return None

    def update_stock(self, product_id: int, new_stock: int) -> bool:
        """Aggiorna lo stock di un prodotto"""
        return self.prodRepo.update_stock(product_id, new_stock)  # Da aggiungere in ProductRepository

    def get_low_stock_products(self, threshold: int = 5) -> List[Dict[str, Any]]:
        """Prodotti con stock basso"""
        products = self.get_all_product()
        return [p for p in products if p.get("stock", 0) <= threshold]