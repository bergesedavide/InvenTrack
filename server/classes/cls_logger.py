from server.database.file_operations import write_log

import os
from datetime import datetime
from pathlib import Path
from colorama import Fore, Back, Style, init

class Logger:
    def __init__(self, file_name: str):
        init()
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.folder = os.path.join(base_dir, "..", "logs")
        os.makedirs(self.folder, exist_ok=True)

        self.file_name = file_name + ".log"
        self.file_path = os.path.join(self.folder, self.file_name)

        if not Path(self.file_path).exists():
            with open(self.file_path, "x"):
                pass  # crea il file

    def info(self, file_name: str,  message: str, date: str):
        color_brackets = Fore.LIGHTBLUE
        message_towrite = color_brackets + "[INFO]" + message
        #write_log()

    def error(self):
        pass

    def calendar_event(self, message: str, date: str):
        color_brackets = Fore.LIGHTBLUE_EX
        print(color_brackets + f"[INFO {date}] " + Style.RESET_ALL + message + "\n")
        message_towrite = f"[INFO {date}] {message}\n"

        write_log("calendar", message_towrite)

    def warning(self):
        pass

    def admin_event(self, message: str,  date: str = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")):
        pass

    

log = Logger("admin")
log.calendar_event("Nuova dataaa")
