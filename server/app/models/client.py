from app.services.calendar_service import CalendarService

from datetime import date

class Client:
    def __init__(self, name: str, surname: str, email: str, password: str, idCity: int, address: str, numAddress: int, dateBirth: date, idGenre: int, card: bool, dateReg: date):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password        #TODO: deve essere già quella hashata
        self.idCity = idCity            #TODO: deve essere già sotto forma di id
        self.address = address
        self.numAddress = numAddress
        self.dateBirth = dateBirth
        self.idGenre = idGenre          #TODO: deve essere già sotto forma di id
        self.card = card                #TODO: deve essere già bool
        self.dateReg = dateReg          #TODO: deve essere presa dal calendario

