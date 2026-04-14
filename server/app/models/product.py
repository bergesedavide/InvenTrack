

class Product:
    def __init__(self, name: str, idCategory: int, price: float, idCompany: int):
        self.name = name
        self.idCategory = idCategory
        self.price = price
        self.idCompany = idCompany


class Category:
    def __init__(self, desc: str):
        self.desc = desc