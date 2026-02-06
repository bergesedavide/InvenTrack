from app.database.database_connection import get_supabase_client
from app.config import DbTables

from enum import Enum

class CityRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.tblAlias = DbTables.CITIES.value

    class DatabaseColName(Enum):
        ID = "id"
        DESC = "desc"
        CAP = "cap"
        LAT = "latitudine"
        LON = "longitudine"
        IDSTATE = "idStato"

    def get_city_by_id(self, idCity: int):
        response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.ID.value, idCity).execute()

        return response.data[0]