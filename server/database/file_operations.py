# TODO: creare funzioni per operare sui file di log
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(BASE_DIR, "..", "logs")

def write_admin(message: str, file_name: str = "admin"):
    pass

def write_log(file_name: str, message: str):
    file_name = file_name + ".log"
    file_path = os.path.join(FOLDER, file_name)

    with open(file_path, "a") as f:
        f.write(message)