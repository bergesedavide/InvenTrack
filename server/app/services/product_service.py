from app.database.product_repository import ProductRepository
from app.database.category_repository import CategoryRepository
from app.database.company_repository import CompanyRepository


class ProductService:
    def __init__(self):
        self.prodRepo = ProductRepository()
        self.catRepo = CategoryRepository()
        self.compRepo = CompanyRepository()
    
    def get_all_product(self):
        product = self.prodRepo.get_all_product()

        for p in product:
            p["name"] = p.pop("nome")
            p["idCategory"] = p.pop("idCategoria")
            p["price"] = p.pop("prezzo")
            p["idCompany"] = p.pop("idAzienda")
    
        return product