from app.database.database_connection import get_supabase_client
from app.config import DbTables
from app.models.gender import Gender

from enum import Enum

class GenderRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.tblAlias = DbTables.GENDERS.value

    class DatabaseColName(Enum):
        COD = "cod"
        DESC = "desc"
        DESC_ENG = "desc_eng"

    def get_genre_by_desc_eng(self, desc_eng: str) -> str:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.COD.value).eq(self.DatabaseColName.DESC_ENG.value, desc_eng).execute()

        if response.data:
            return response.data[0][self.DatabaseColName.COD.value]