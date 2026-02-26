from app.database.database_connection import get_supabase_client
from app.config import DbTables
from app.utils.data_types_creation import DataManipulation
from app.models.city import City

from enum import Enum

class CityRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.tblAlias = DbTables.CITIES.value
        self.dataManipulator = DataManipulation()

    class DatabaseColName(Enum):
        ID = "id"
        DESC = "desc"
        IDSTATE = "idStato"
        CAP = "cap"
        LAT = "latitudine"
        LON = "longitudine"

    def get_city_by_id(self, idCity: int):
        response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.ID.value, idCity).execute()
        response = response.data[0]

        city = City(response["desc"], response["idStato"], response["cap"], response["latitudine"], response["longitudine"])
        return city
    
    def get_id_by_desc(self, city: City) -> int:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).eq(self.DatabaseColName.DESC.value, city.desc).execute()
        
        if not response.data:
            idCity = self.save(city)
            return idCity
        else:    
            return int(response.data[0][self.DatabaseColName.ID.value])
    
    def save(self, city: City):
        keys = [self.DatabaseColName.DESC.value, self.DatabaseColName.IDSTATE.value, self.DatabaseColName.CAP.value, 
                self.DatabaseColName.LAT.value, self.DatabaseColName.LON.value]

        values = [city.desc, city.idState, city.cap, city.lat, city.lon]

        db_dict = self.dataManipulator.todict(keys, values)

        response = self.db.table(self.tblAlias).insert(db_dict).execute()

        return int(response.data[0][self.DatabaseColName.ID.value])