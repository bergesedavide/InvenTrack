from app.database.database_connection import get_supabase_client
from app.models.client import Client
from app.config import DbTables

from enum import Enum

class ClientRepository:
    def __init__(self):
        self.db = get_supabase_client()
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
    
    def save(client: Client):
        pass