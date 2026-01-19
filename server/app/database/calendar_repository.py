from app.database.calendar_operations import CalendarOperation
from app.models.calendar import Calendar
from app.services.logger_service import LoggerService
from app.config import LogFile

class CalendarRepository:
    def __init__(self):
        self.logger = LoggerService()
        self.filename = LogFile.CALENDAR.value
        self.db = CalendarOperation()

    def load(self) -> Calendar:
        date = self.db.get_date()
        return Calendar(
            day = int(date["day"]),
            month = int(date["month"]),
            year = int(date["year"]),
            week_day = int(date["week_day"])
        )

    def save(self, calendar: Calendar):
        self.db.set_date(calendar.day, calendar.month, calendar.year, calendar.week_day, calendar.can_ship())
        self.logger.info(self.filename, "Nuova data salvata nel database")