from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.config import DbTables

from enum import Enum

class StatesOperation():
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()
        self.tblAlias = DbTables.STATES.value

    class DatabaseColName(Enum):
        ID = "id"
        DESC = "desc"

    # Get
    def get_state(self, colId: DatabaseColName = None, colName: DatabaseColName = None, colOrder: DatabaseColName = None):
        
        if colOrder:
            response = self.db.table(self.tblAlias).select("*").order(colOrder.value).execute()
        else:
            response = self.db.table(self.tblAlias).select("*").execute()

        states = []
        for row in response.data:
            state_id = row[self.DatabaseColName.ID.value]
            state_name = row[self.DatabaseColName.DESC.value]

            state_dict = {}
            if colId:
                state_dict[self.DatabaseColName.ID.value] = state_id
            if colName:
                state_dict[self.DatabaseColName.DESC.value] = state_name

            states.append(state_dict)

        return states