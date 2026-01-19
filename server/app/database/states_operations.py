from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from enum import Enum

class StatesOperation():
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()

    class DatabaseColName(Enum):
        ID = "id"
        NAME = "name"
        ALPH_ORDER = "alphabetic_order"

    # Get
    def get_state(self, colId: DatabaseColName = None, colName: DatabaseColName = None, colOrder: DatabaseColName = None):
        
        if colOrder:
            response = self.db.table("states").select("*").order(colOrder.value).execute()
        else:
            response = self.db.table("states").select("*").execute()

        states = []
        for row in response.data:
            state_id = row[self.DatabaseColName.ID.value]
            state_name = row[self.DatabaseColName.NAME.value]

            state_dict = {}
            if colId:
                state_dict[self.DatabaseColName.ID.value] = state_id
            if colName:
                state_dict[self.DatabaseColName.NAME.value] = state_name

            states.append(state_dict)

        return states