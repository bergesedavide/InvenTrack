from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.config import DbTables
from app.models.role import Role

from enum import Enum

class RoleRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()
        self.tblAlias = DbTables.ROLES.value

    class DatabaseColName(Enum):
        ID = "id"
        DESC = "desc"

    def get_id_by_desc(self, desc: str) -> int:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).execute()

        if response.data:
            return int(response.data[0][self.DatabaseColName.ID.value])
        
    def get_all_id(self) -> list[int]:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).execute()

        rows = response.data
        ids = [row[self.DatabaseColName.ID.value] for row in rows]

        return ids
        
    def save(self, role: Role):
        keys = [self.DatabaseColName.ID.value, self.DatabaseColName.DESC.value]
        values = [role.idRole, role.desc]

        db_dict = self.dataManipulator.todict(keys, values)

        self.db.table(self.tblAlias).insert(db_dict).execute()