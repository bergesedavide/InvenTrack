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
    
    def get_by_email(self, email: str):
        """Recupera un boss per email"""
        response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.EMAIL.value, email).execute()
        
        if response.data:
            boss = response.data[0]
            return {
                "id": boss.get(self.DatabaseColName.ID.value),
                "surname": boss.get(self.DatabaseColName.SURNAME.value),
                "name": boss.get(self.DatabaseColName.NAME.value),
                "email": boss.get(self.DatabaseColName.EMAIL.value),
                "password": boss.get(self.DatabaseColName.PWD.value),
                "birthDate": boss.get(self.DatabaseColName.DATEBIRTH.value),
                "birthState": boss.get(self.DatabaseColName.STATEBIRTH.value)
            }
        return None