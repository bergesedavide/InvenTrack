

class Client:
    def __init__(self, name: str, surname: str, email: str, password: str, dateBirth: str, card: bool, idCity: int, codGender: str, address: str, numAddress: int, dateReg: str):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.dateBirth = dateBirth
        self.card = card
        self.idCity = idCity
        self.codGender = codGender
        self.address = address
        self.numAddress = numAddress
        self.dateReg = dateReg


class Gender:
    def __init__(self, cod, desc, desc_eng):
        self.cod = cod
        self.desc = desc
        self.desc_eng = desc_eng