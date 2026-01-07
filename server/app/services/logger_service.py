from app.config import LogLevel
from app.database.logger_repository import LoggerRepository
from app.models.logger import Logger

class LoggerService():
    RESET_COLOR = LogLevel.RESET.value

    def __init__(self):
        self.repo = LoggerRepository()

    def log(self, filename: str, message: str, level: LogLevel = None):
        self.logger = Logger(filename)
        if level is None:
            level = LogLevel.INFO
        
        print(f"{level.value} [{level.name}] {message}{self.RESET_COLOR}")
        self.repo.write_log(filename, level.name, message)

    def debug(self, filename: str, message: str):
        self.log(filename, message, LogLevel.DEBUG)

    def info(self, filename: str, message: str):
        self.log(filename, message, LogLevel.INFO)

    def warning(self, filename: str, message: str):
        self.log(filename, message, LogLevel.WARNING)

    def error(self, filename: str, message: str):
        self.log(filename, message, LogLevel.ERROR)