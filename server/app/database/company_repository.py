from app.database.database_connection import get_supabase_client
from app.utils.data_types_creation import DataManipulation
from app.models.company import Company
from app.config import DbTables

from enum import Enum

class CompanyRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.dataManipulator = DataManipulation()
        self.tblAlias = DbTables.COMPANY.value

    class DatabaseColName(Enum):
        ID = "id"
        NAME = "nome"
        IDBOSS = "idCapoAziendale"
        IDCITY = "idCity"
        IDPRICING = "idPianoRegistrazione"
        DATEREG = "dataRegistrazione"
        EMAIL = "email"
        PHONE = "telefono"
        LOGO = "logo"
        CHATBOT = "chatbot"
        BUSINESSANALISYS = "businessAnalysis"
        CHECKPRICE = "controlloPrezzi"

    def get_company_by_id(self, idCompany: int) -> Company:
        response = self.db.table(self.tblAlias).select("*").eq(self.DatabaseColName.ID.value, idCompany).execute()
        response = response.data[0]
        
        company = Company(response[self.DatabaseColName.NAME.value], response[self.DatabaseColName.IDBOSS.value], response[self.DatabaseColName.IDCITY.value], response[self.DatabaseColName.IDPRICING.value], response[self.DatabaseColName.DATEREG.value],
                          response[self.DatabaseColName.EMAIL.value], response[self.DatabaseColName.PHONE.value], response[self.DatabaseColName.LOGO.value], response[self.DatabaseColName.CHATBOT.value], response[self.DatabaseColName.BUSINESSANALISYS.value],
                          response[self.DatabaseColName.CHECKPRICE.value])
        
        return company

    def get_id_by_desc(self, desc: str) -> int:
        response = self.db.table(self.tblAlias).select(self.DatabaseColName.ID.value).eq(self.DatabaseColName.DESC.value, desc).execute()

        if response.data:
            return int(response.data[0][self.DatabaseColName.ID.value])

    def save(self, company: Company):
        keys = [self.DatabaseColName.NAME.value, self.DatabaseColName.IDBOSS.value, self.DatabaseColName.IDCITY.value, self.DatabaseColName.IDPRICING.value, self.DatabaseColName.DATEREG.value, self.DatabaseColName.EMAIL.value,
                self.DatabaseColName.PHONE.value, self.DatabaseColName.LOGO.value, self.DatabaseColName.CHATBOT.value, self.DatabaseColName.BUSINESSANALISYS.value, self.DatabaseColName.CHECKPRICE.value]
        values = [company.name, company.idBoss, company.idCity, company.idPricing, company.dateReg, company.email, company.phone, company.logo, company.chatbot, company.businessAnalysis, company.checkPrice]

        db_dict = self.dataManipulator.todict(keys, values)

        self.db.table(self.tblAlias).insert(db_dict).execute()