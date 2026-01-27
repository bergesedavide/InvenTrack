from app.database.calendar_operations import CalendarOperation
from app.models.calendar import Calendar
from app.services.logger_service import LoggerService
from app.config import LogFile

from datetime import datetime

class CalendarRepository:
    def __init__(self):
        self.logger = LoggerService()
        self.filename = LogFile.CALENDAR.value
        self.db = CalendarOperation()
        self.colName = self.db.DatabaseColName

    def load(self) -> Calendar:
        date = self.db.get_date()
        return Calendar(
            day = int(date[self.colName.DAY.value]),
            month = int(date[self.colName.MONTH.value]),
            year = int(date[self.colName.YEAR.value]),
            week_day = int(date[self.colName.WEEK_DAY.value])
        )

    def save(self, calendar: Calendar):
        self.db.set_date(calendar)
        self.logger.info(self.filename, "Nuova data salvata nel database", datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))