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
        DATEBIRTH = "dataNascita"
        CARD = "tessera"
        IDCITY = "idCitta"
        CODGENDER = "codGenere"
        ADDRESS = "indirizzo"
        NUMADDRESS = "numeroCivico"
        DATEREG = "dataReg"

    def get_client_by_id(self, idClient: int) -> Client:
        response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.ID.value, idClient).execute()
        response = response.data[0]
        
        client = Client(response[self.DatabaseColName.NAME.value], response[self.DatabaseColName.SURNAME.value], response[self.DatabaseColName.EMAIL.value], response[self.DatabaseColName.PWD.value], response[self.DatabaseColName.DATEBIRTH.value],
                        response[self.DatabaseColName.CARD.value], response[self.DatabaseColName.IDCITY.value], response[self.DatabaseColName.CODGENDER.value], response[self.DatabaseColName.ADDRESS.value], response[self.DatabaseColName.NUMADDRESS.value],
                        response[self.DatabaseColName.DATEREG.value])
        
        return client
    
    def get_all_id(self) -> list[int]:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).execute()

        rows = response.data
        ids = [row[self.DatabaseColName.ID.value] for row in rows]

        return ids
    
    def save(self, client: Client):
        keys = [self.DatabaseColName.NAME.value, self.DatabaseColName.SURNAME.value,
                     self.DatabaseColName.EMAIL.value, self.DatabaseColName.PWD.value,
                     self.DatabaseColName.DATEBIRTH.value, self.DatabaseColName.CARD.value,
                     self.DatabaseColName.IDCITY.value, self.DatabaseColName.CODGENDER.value, 
                     self.DatabaseColName.ADDRESS.value, self.DatabaseColName.NUMADDRESS.value, 
                     self.DatabaseColName.DATEREG.value]
        values = [client.name, client.surname, client.email, client.password, client.dateBirth, 
                  client.card, client.idCity, client.codGender, client.address, client.numAddress, 
                  client.dateReg]
        
        db_dict = self.dataManipulator.todict(keys, values)

        self.db.table(self.tblAlias).insert(db_dict).execute()