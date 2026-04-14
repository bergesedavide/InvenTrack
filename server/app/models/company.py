

class Company:
    def __init__(self, name: str, idBoss: int, idCity: int, idPricing: int, dateReg: str, chatbot: bool, businessAnalysis: bool, checkPrice: bool, email: str = None, phone: str = None, logo: str = None):
        self.name = name
        self.idBoss = idBoss
        self.idCity = idCity
        self.idPricing = idPricing
        self.dateReg = dateReg
        self.chatbot = chatbot
        self.businessAnalysis = businessAnalysis
        self.checkPrice = checkPrice
        
        self.email = email
        self.phone = phone
        self.logo = logo


class PricingPlan:
    def __init__(self, desc: str):
        self.desc = desc