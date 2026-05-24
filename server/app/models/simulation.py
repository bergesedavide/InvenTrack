from datetime import datetime

class SimulationState:
    def __init__(self, attiva: bool = False, ultimo_aggiornamento: datetime = None, 
                 ordini_generati: int = 0, clienti_generati: int = 0, movimenti_stock: int = 0):
        self.id = 1  # singola riga
        self.attiva = attiva
        self.ultimo_aggiornamento = ultimo_aggiornamento or datetime.now()
        self.ordini_generati = ordini_generati
        self.clienti_generati = clienti_generati
        self.movimenti_stock = movimenti_stock