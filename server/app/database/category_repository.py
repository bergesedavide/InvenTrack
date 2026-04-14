from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.models.product import Category
from app.config import DbTables

from enum import Enum

class CategoryRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.tblAlias = DbTables.CATEGORIES.value
        self.dataManipulator = DataManipulation()

    class DatabaseColName(Enum):
        ID = "id"
        DESC = "name"

    def get_desc_by_id(self, idCategory: int) -> str:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.DESC.value).eq(self.DatabaseColName.ID.value, idCategory).execute()
        
        if response.data:
            return int(response.data[0][self.DatabaseColName.ID.value])

    def get_id_by_desc(self, desc: str) -> int:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).eq(self.DatabaseColName.DESC.value, desc).execute()

        if response.data:
            return int(response.data[0][self.DatabaseColName.ID.value])

    def save(self, category: Category):
        keys = [self.DatabaseColName.DESC.value]
        values = [category.desc]

        db_dict = self.dataManipulator.todict(keys, values)
        
        self.db.table(self.tblAlias).insert(db_dict).execute()