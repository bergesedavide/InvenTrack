from threading import Thread
from calendar_opt import get_calendar 

class Order_Thread:
    def __init__(self):
        # Calendario
        complete_date = get_calendar()["date"]
        week_day = complete_date.split(" - ")[0].split(" ")[0]
        day = complete_date.split(" - ")[0].split(" ")[1]
        month = complete_date.split(" - ")[1]
        self.date = {"week_day": week_day, "day": day, "month": month}
        self.can_ship = get_calendar()["shipping"]

        # Thread
        self.quantity = 25  # todo -> fare calcolo legato a numero filiali

        # Prodotti
        # products = get dati da database 



    def printDate(self):
        print(f"{self.date['day']} - {self.date['month']} | Can Ship? {self.can_ship}")

ordine = Order_Thread()
ordine.printDate()
