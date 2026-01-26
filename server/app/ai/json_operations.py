import os

class JsonOperations:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # SALVARE LA LOCATION IN BASE ALLA IA CHE STA CHIAMANDO IL PROCESSO

    def __init__(self):
        self.loc = 0