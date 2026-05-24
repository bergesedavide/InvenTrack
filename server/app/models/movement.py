class Movement:
    def __init__(self, idProdotto: int, tipo: str, quantita: int, data: str, prezzo_unitario: float = None, note: str = None):
        """
        tipo può essere: 'entrata', 'uscita', 'ordine', 'scarto'
        """
        self.idProdotto = idProdotto
        self.tipo = tipo
        self.quantita = quantita
        self.data = data
        self.prezzo_unitario = prezzo_unitario
        self.note = note