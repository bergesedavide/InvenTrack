from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.config import DbTables
from app.models.state import State

from enum import Enum

class StateRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.tblAlias = DbTables.STATES.value
        self.dataManipulator = DataManipulation()

    class DatabaseColName(Enum):
        ID = "id"
        DESC = "desc"

    def get_id_by_desc(self, desc: str) -> int:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).eq(self.DatabaseColName.DESC.value, desc).execute()

        if response.data:
            return int(response.data[0][self.DatabaseColName.ID.value])
        else:
            return {"message": f"Ricerca fallita, lo stato {desc} non esiste"}