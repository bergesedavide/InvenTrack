# Variabili globali
# gestire gli eventi tramite database per scontistica
from database.db_operations import insert_discount
from calendar_opt import get_calendar, change_style_calendar

class Discount:
    def __init__(self, name, discount, start, end, categories):
        self.name = name
        self.discount = discount
        self.start = start
        self.end = end
        self.categories = categories

        calendar = get_calendar()["date"].replace(" - ", "-").split(" ")[1]
        calendar = change_style_calendar(calendar)

        date_cod, date_message = self._check_dates(calendar)

        if int(date_cod) == 404: ValueError(date_message)
        
        # TODO: continuare con altri controlli post date --> Categorie, valori

       
    def add_to_db(self):
            # costruire metodo di accesso per il db
            discount = []
            insert_discount(discount)
            return {"message": "Sconto inserito correttamente"}
    
    def _check_dates(self, calendar):
        # funzioni di calcolo
        if self.start < calendar:
            return {"message": "Non puoi selezionare come 'data di inizio sconto' una data passata", "cod": 404}
        if self.end < self.start:
            return {"message": "Non puoi selezionare come 'data di fine sconto' una data minore della 'data di inizio sconto'", "cod": 404}
        return {"message": "Le date impostate vanno bene", "cod": 200}

    def check_categories(self):
        return 0