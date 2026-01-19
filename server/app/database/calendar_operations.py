from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from enum import Enum

class CalendarOperation:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()
        
    class DatabaseColName(Enum):
        ID = "id"
        DAY = "day"
        MONTH = "month"
        YEAR = "year"
        WEEK_DAY = "week_day"
        SHIP = "shipping"

    # Get
    def get_date(self, col: DatabaseColName = None):
        response = self.db.table("calendar").select("*").execute()

        if col == self.DatabaseColName.DAY:
            return int(response.data[0][self.DatabaseColName.DAY.value])
        
        if col == self.DatabaseColName.MONTH:
            return int(response.data[0][self.DatabaseColName.MONTH.value])
        
        if col == self.DatabaseColName.YEAR:
            return int(response.data[0][self.DatabaseColName.YEAR.value])
        
        if col == self.DatabaseColName.WEEK_DAY:
            return int(response.data[0][self.DatabaseColName.WEEK_DAY.value])
        
        if col == self.DatabaseColName.SHIP.value:
            return bool(response.data[0][self.DatabaseColName.SHIP.value])
        
        if not col:
            return response.data[0]

    # Update
    def set_date(self, day: int, month: int, year: int, week_day: int, ship: bool):
        col = [self.DatabaseColName.DAY.value, self.DatabaseColName.MONTH.value, self.DatabaseColName.YEAR.value, self.DatabaseColName.WEEK_DAY.value, self.DatabaseColName.SHIP.value]
        values = [day, month, year, week_day, ship]

        db_dict = self.dataManipulator.todict(col, values)

        self.db.table("calendar").update(db_dict).eq(self.DatabaseColName.ID.value, 1).execute()