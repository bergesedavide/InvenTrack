from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.models.boss import Boss
from app.config import DbTables

from enum import Enum

class BossRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()
        self.tblAlias = DbTables.BOSSES.value

    class DatabaseColName(Enum):
        ID = "id"
        SURNAME = "cognome"
        NAME = "nome"
        EMAIL = "email"
        PWD = "password"
        DATEBIRTH = "dataNascita"
        STATEBIRTH = "statoNascita"


    def get_email_password(self) -> list[dict[str, str]]:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.EMAIL.value, self.DatabaseColName.PWD.value).execute()
        
        return response.data
    
    def save(self, boss: Boss):
        keys = [self.DatabaseColName.SURNAME.value, self.DatabaseColName.NAME.value, self.DatabaseColName.EMAIL.value, self.DatabaseColName.PWD.value,
                self.DatabaseColName.DATEBIRTH.value, self.DatabaseColName.STATEBIRTH.value]
        values = [boss.surname, boss.name, boss.email, boss.password, boss.birthDate, boss.birthState]

        db_dict = self.dataManipulator.todict(keys, values)

        self.db.table(self.tblAlias).insert(db_dict).execute()
    