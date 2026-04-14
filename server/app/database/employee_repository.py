from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.config import DbTables
from app.models.employee import Employee

from enum import Enum

class EmployeeRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()
        self.tblAlias = DbTables.EMPLOYEES.value

    class DatabaseColName(Enum):
        ID = "id"
        SURNAME = "cognome"
        NAME = "nome"
        EMAIL = "email"
        PWD = "password"
        IDROLE = "idRuolo"
        IDWORKPLACE = "idPostoLavoro"

    def save(self, employee: Employee):
        keys = [self.DatabaseColName.SURNAME.value, self.DatabaseColName.NAME.value, self.DatabaseColName.EMAIL.value,
                self.DatabaseColName.PWD.value, self.DatabaseColName.IDROLE.value, self.DatabaseColName.IDWORKPLACE.value]
        
        values = [employee.surname, employee.name, employee.email, employee.password, employee.idRole, employee.idWorkPlace]

        db_dict = self.dataManipulator.todict(keys, values)
        
        self.db.table(self.tblAlias).insert(db_dict).execute()

    def get_email_password(self) -> list[dict[str, str]]:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.EMAIL.value, self.DatabaseColName.PWD.value).execute()
        
        return response.data