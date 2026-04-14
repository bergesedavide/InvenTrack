

class Employee:
    def __init__(self, surname: str, name: str, email: str, password: str, idRole: int = None, idWorkPlace: int = None):
        self.surname = surname
        self.name = name
        self.email = email
        self.password = password
        self.idRole = idRole
        self.idWorkPlace = idWorkPlace


class Role:
    def __init__(self, idRole: int, desc: str):
        self.idRole = idRole
        self.desc = desc