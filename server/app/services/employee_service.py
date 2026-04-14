from app.database.employee_repository import EmployeeRepository
from app.models.employee import Employee
from app.database.role_repository import RoleRepository
from app.utils.utility_generator import generate_password

class EmployeeService:
    def __init__(self):
        self.employeeRepo = EmployeeRepository()
        self.roleRepo = RoleRepository()

    def add_employee(self, surname: str, name: str, email: str, password: str = None, role: str = None, workPlace: str = None):
        
        if not password:
            password = generate_password()
        
        idRole = None
        if role:
            idRole = self.roleRepo.get_id_by_desc(role)

        idWorkPlace = None
        if workPlace:
            #TODO: (per dopo) trovare l'id corrispondente a quel posto di lavoro
            pass

        emp = Employee(surname, name, email, password, idRole, idWorkPlace)

        self.employeeRepo.save(emp)