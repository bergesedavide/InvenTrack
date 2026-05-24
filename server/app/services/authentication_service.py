from app.database.boss_repository import BossRepository
from app.database.employee_repository import EmployeeRepository
from app.core.security import verify_password

class AuthenticationService:
    def __init__(self):
        self.bossRepo = BossRepository()
        self.emplRepo = EmployeeRepository()

    def authenticate(self, email: str, password: str) -> dict:
        """Restituisce dati utente se login OK, altrimenti None"""
        if not email or not password:
            return None
        
        bosses = self.bossRepo.get_email_password()
        workers = self.emplRepo.get_email_password()

        for user in bosses:
            if user["email"] == email and verify_password(password, user["password"]):
                return {"id": user.get("id"), "type": "boss"}
        
        for user in workers:
            if user["email"] == email and verify_password(password, user["password"]):
                return {"id": user.get("id"), "type": "employee"}
        
        return None

    def check_login(self, email: str, password: str) -> bool:
        """Metodo legacy per compatibilità"""
        return self.authenticate(email, password) is not None