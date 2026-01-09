import os
from pathlib import Path
from app.config import directory_log

class Logger():
    FOLDER = directory_log()
        
    def __init__(self, filename: str):
        os.makedirs(self.FOLDER, exist_ok=True)

        self.filename = filename
        self.filepath = os.path.join(self.FOLDER, self.filename)

        if not Path(self.filepath).exists():
            with open(self.filepath, "x"):
                print("File creato")