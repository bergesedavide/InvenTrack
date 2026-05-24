from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.models.product import Product
from app.config import DbTables

from enum import Enum

class ProductRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()
        self.tblAlias = DbTables.PRODUCTS.value

    class DatabaseColName(Enum):
        ID = "id"
        NAME = "nome"
        IDCATEGORY = "idCategoria"
        PRICE = "prezzo"
        IDCOMPANY = "idAzienda"

    def get_all_product(self, idCategory: int = None):
        if idCategory:
            response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.IDCATEGORY.value, idCategory).execute()
        else:
            response = self.db.table(self.tblAlias).select("*").execute()

        if response.data:
            return response.data
        return []
        
    def get_all_product_by_id(self, idCategory: int):
        if idCategory:
            response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.IDCATEGORY.value, idCategory).execute()

        if response.data:
            return response.data

    def save(self, product: Product):
        keys = [self.DatabaseColName.ID.value, self.DatabaseColName.NAME.value, self.DatabaseColName.IDCATEGORY.value, self.DatabaseColName.PRICE.value, self.DatabaseColName.IDCOMPANY.value]
        values = [product.name, product.idCategory, product.price, product.idcompany]

        db_dict = self.dataManipulator.todict(keys, values)

        self.db.table(self.tblAlias).insert(db_dict).execute()

    def get_product_by_id(self, product_id: int):
        """Recupera un singolo prodotto per ID"""
        response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.ID.value, product_id).execute()
        
        if response.data:
            product = response.data[0]
            return {
                "id": product.get(self.DatabaseColName.ID.value),
                "name": product.get(self.DatabaseColName.NAME.value),
                "idCategory": product.get(self.DatabaseColName.IDCATEGORY.value),
                "price": product.get(self.DatabaseColName.PRICE.value),
                "idCompany": product.get(self.DatabaseColName.IDCOMPANY.value)
            }
        return None