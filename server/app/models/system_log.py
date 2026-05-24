from datetime import datetime

class SystemLog:
    def __init__(self, livello: str, messaggio: str, data: datetime = None):
        """
        livello può essere: 'DEBUG', 'INFO', 'WARNING', 'ERROR'
        """
        self.livello = livello
        self.messaggio = messaggio
        self.data = data or datetime.now()