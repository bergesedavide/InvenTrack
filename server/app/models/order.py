class Order:
    def __init__(self, codice: str, idCliente: int, idAzienda: int, data: str, totale: float = 0, status: str = "PENDING"):
        self.codice = codice
        self.idCliente = idCliente
        self.idAzienda = idAzienda
        self.data = data
        self.totale = totale
        self.status = status


class OrderDetail:
    def __init__(self, idOrdine: int, idProdotto: int, quantita: int, prezzo_unitario: float):
        self.idOrdine = idOrdine
        self.idProdotto = idProdotto
        self.quantita = quantita
        self.prezzo_unitario = prezzo_unitario
        self.subtotale = quantita * prezzo_unitario