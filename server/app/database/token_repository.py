from app.database.database_connection import get_supabase_client
from app.services.calendar_service import CalendarService
from app.config import DbTables
from datetime import datetime
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

    def get_tokens(self) -> list:
        """Recupera tutti i token"""
        response = self.db.table(DbTables.TOKENS.value).select(self.DatabaseColName.TOKEN.value).execute()
        
        tokens = []
        for row in response.data:
            token = row[self.DatabaseColName.TOKEN.value]
            tokens.append(token)
        
        return tokens

    def get_token_by_email(self, email: str) -> str:
        """Recupera il token di un utente per email"""
        response = self.db.table(DbTables.TOKENS.value).select(self.DatabaseColName.TOKEN.value).eq(self.DatabaseColName.EMAIL.value, email).execute()
        
        if response.data:
            return response.data[0][self.DatabaseColName.TOKEN.value]
        return None

    def set_token(self, email: str, token: str) -> dict:
        """Salva un nuovo token (sovrascrive se esiste)"""
        date = self.cal.get_date()
        
        # Cancella token esistente per questa email
        self.db.table(DbTables.TOKENS.value).delete().eq(self.DatabaseColName.EMAIL.value, email).execute()
        
        # Inserisci nuovo token
        dbToken = {
            self.DatabaseColName.EMAIL.value: email,
            self.DatabaseColName.TOKEN.value: token,
            self.DatabaseColName.CREATED_AT.value: date
        }
        
        response = self.db.table(DbTables.TOKENS.value).insert(dbToken).execute()
        return response.data[0] if response.data else {}

    def delete_token(self, email: str) -> bool:
        """Cancella il token di un utente"""
        response = self.db.table(DbTables.TOKENS.value).delete().eq(self.DatabaseColName.EMAIL.value, email).execute()
        return len(response.data) > 0

    def is_token_valid(self, token: str) -> bool:
        """Verifica se un token esiste nel database"""
        response = self.db.table(DbTables.TOKENS.value).select(self.DatabaseColName.ID.value).eq(self.DatabaseColName.TOKEN.value, token).execute()
        return len(response.data) > 0