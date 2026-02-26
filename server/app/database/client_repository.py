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

        self.keys = [self.DatabaseColName.NAME.value, self.DatabaseColName.SURNAME.value,
                     self.DatabaseColName.EMAIL.value, self.DatabaseColName.PWD.value,
                     self.DatabaseColName.DATEBIRTH.value, self.DatabaseColName.CARD.value,
                     self.DatabaseColName.IDCITY.value, self.DatabaseColName.CODGENDER.value, 
                     self.DatabaseColName.ADDRESS.value, self.DatabaseColName.NUMADDRESS.value, 
                     self.DatabaseColName.DATEREG.value]

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
        
        client = Client(response["nome"], response["cognome"], response["email"], response["password"], response["dataNascita"],
                        response["tessera"], response["idCitta"], response["codGenere"], response["indirizzo"], response["numeroCivico"],
                        response["dataReg"])
        
        return client
    
    def get_all_id(self) -> list[int]:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).execute()

        rows = response.data
        ids = [row[self.DatabaseColName.ID.value] for row in rows]

        return ids
    
    def save(self, client: Client):
        values = [client.name, client.surname, client.email, client.password, client.dateBirth, 
                  client.card, client.idCity, client.codGender, client.address, client.numAddress, 
                  client.dateReg]
        
        db_dict = self.dataManipulator.todict(self.keys, values)

        self.db.table(self.tblAlias).insert(db_dict).execute()