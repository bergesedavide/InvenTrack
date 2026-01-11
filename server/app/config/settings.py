from enum import Enum
from colorama import init, Style, Fore
import os

init()

# ----------------------------
# CLASSI
# ----------------------------

class DataTypes(Enum):
    STRING = str
    INTEGER = int
    FLOAT = float
    BOOLEAN = bool


class LogLevel(Enum):
    DEBUG = Fore.GREEN         # verde
    INFO = Fore.LIGHTBLUE_EX   # azzurro
    WARNING = Fore.YELLOW      # giallo
    ERROR = Fore.RED           # rosso
    RESET = Style.RESET_ALL    # reset colore

class LogFile(Enum):
    CALENDAR = "calendar.log"
    USER = "user.log"

# da studiare
class UserRoles(Enum):
    ADMIN = 1

class AiModel(Enum):
    TRASPORTI = "AI_MODEL_TRASPORTI"

# ----------------------------
# FUNZIONI
# ----------------------------

def directory_log():
    directories = ["config", "database", "logs", "models", "routes", "services"]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    split = base_dir.split("\\")
    current_dir = split[len(split) - 1]
    
    if current_dir in directories:
        return os.path.join(base_dir, "..", "logs")
    else:
        return {"message": "Posizione di accesso non supportata"}
    
def list_domain():
    # TODO: probabile necessità di richiamo di un database
    return []