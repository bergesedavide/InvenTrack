from app.database.user_operation import UserOperation
from enum import Enum

class UserRepository:
    def __init__(self):
        self.db =  UserOperation()

    class DatabaseColName(Enum):
        ID = "id"
        EMAIL = "email"

    def load(self):
        # Scaricare dal database email e password
        
        pass

    def check_login(self, email, pwd):
        pass