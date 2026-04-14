from app.database.boss_repository import BossRepository
from app.database.employee_repository import EmployeeRepository

class AuthenticationService:
    def __init__(self):
        self.bossRepo = BossRepository()
        self.emplRepo = EmployeeRepository()

    def check_login(self, email: str, password: str) -> dict:

        if not email or not password:
            return False
        
        bosses = self.bossRepo.get_email_password()
        workers = self.emplRepo.get_email_password()

        #workers = [{"email": "ddd", "password": "ddd"}]

        users = bosses + workers
        print(users)

        for user in users:
            if user["email"] == email and user["password"] == password:
                return True
            
        return False