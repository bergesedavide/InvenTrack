from app.config import LogLevel
from app.database.logger_repository import LoggerRepository
from app.models.logger import Logger

class LoggerService():
    RESET_COLOR = LogLevel.RESET.value

    def __init__(self):
        self.repo = LoggerRepository()

    def log(self, filename: str, message: str, date = None, level: LogLevel = None):
        self.logger = Logger(filename)
        if level is None:
            level = LogLevel.INFO
        
        if not date:
            print(f"{level.value} [{level.name}]{self.RESET_COLOR} {message}")
            self.repo.write_log(filename, level.name, message)
        else:
            print(f"{level.value} [{level.name} | {date}]{self.RESET_COLOR} {message}")
            self.repo.write_log(filename, level.name, message, date)

    def debug(self, filename: str, message: str, date = None):
        self.log(filename, message, date, LogLevel.DEBUG)

    def info(self, filename: str, message: str, date = None):
        self.log(filename, message, date, LogLevel.INFO)

    def warning(self, filename: str, message: str, date = None):
        self.log(filename, message, date, LogLevel.WARNING)

    def error(self, filename: str, message: str, date = None):
        self.log(filename, message, date, LogLevel.ERROR)