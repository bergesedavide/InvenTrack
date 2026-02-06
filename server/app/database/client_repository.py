from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.models.client import Client
from app.config import DbTables

from enum import Enum

class ClientRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()
        self.tblAlias = DbTables.CLIENTS.value

    class DatabaseColName(Enum):
        ID = "id"
        NAME = "nome"
        SURNAME = "cognome"
        EMAIL = "email"
        PWD = "password"
        IDCITY = "idCitta"
        ADDRESS = "indirizzo"
        NUMADDRESS = "numeroCivico"
        DATEBIRTH = "dataNascita"
        IDGENRE = "idGenere"
        CARD = "tessera"
        DATEREG = "dataReg"

    def get_client_by_id(self, idClient: int):
        response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.ID.value, idClient).execute()
        
        return response.data[0]
    
    def get_all_id(self):
        rows = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).fetchall()
        ids = [row[0] for row in rows]

        return ids
    
    def save(self, client: Client):
        keys = [self.DatabaseColName.NAME.value, self.DatabaseColName.SURNAME.value,
                self.DatabaseColName.EMAIL.value, self.DatabaseColName.PWD.value,
                self.DatabaseColName.IDCITY.value, self.DatabaseColName.ADDRESS.value,
                self.DatabaseColName.NUMADDRESS.value, self.DatabaseColName.DATEBIRTH.value,
                self.DatabaseColName.IDGENRE.value, self.DatabaseColName.CARD.value,
                self.DatabaseColName.DATEREG.value]
        
        values = [client.name, client.surname, client.email, client.password, client.idCity,
                  client.address, client.numAddress, client.dateBirth, client.idGenre,
                  client.card, client.dateReg]
        
        db_dict = self.dataManipulator.todict(keys, values)

        self.db.table(self.tblAlias).insert(db_dict).execute()