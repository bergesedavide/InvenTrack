from server.database.db_operations import insert_branch

class Branches:
    def __init__(self, name):
        self.name = name

    def printName(self):
        print(self.name)

    def add_database(self):
        branc = None
        insert_branch(branc)


azienda = Branches("Caporale")
azienda.printName()