from app.database.database_connection import get_supabase_client
from app.services.calendar_service import CalendarService
from enum import Enum

class TokenRepository:
    def __init__(self):
        self.db = get_supabase_client()
        self.cal = CalendarService()

    class DatabaseColName(Enum):
        ID = "id"
        EMAIL = "email"
        TOKEN = "token"
        CREATED_AT = "created_at"

    def get_tokens(self):
        
        response = self.db.table("tokens").select(self.DatabaseColName.TOKEN.value).execute()

        tokens = []
        for row in response.data:
            token = row[self.DatabaseColName.TOKEN.value]
            tokens.append(token)

        return tokens
    
    def set_token(self, email: str, token: str):
        date = self.cal.get_date()

        dbToken = {
            self.DatabaseColName.EMAIL.value: email,
            self.DatabaseColName.TOKEN.value: token,
            self.DatabaseColName.CREATED_AT.value: date
        }

        response = self.db.table("tokens").insert(dbToken).execute()
        print(response.data)
