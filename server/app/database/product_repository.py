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

    def get_all_product(self):
        response = self.db.table(self.tblAlias).select("*").execute()
        
        if response.data:
            return response.data


    def save(self, product: Product):
        keys = [self.DatabaseColName.ID.value, self.DatabaseColName.NAME.value, self.DatabaseColName.IDCATEGORY.value, self.DatabaseColName.PRICE.value, self.DatabaseColName.IDCOMPANY.value]
        values = [product.name, product.idCategory, product.price, product.idcompany]

        db_dict = self.dataManipulator.todict(keys, values)

        self.db.table(self.tblAlias).insert(db_dict).execute()