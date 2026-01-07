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
        return Calendar(
            day = self.db.get_day(),
            month = self.db.get_month(),
            year = self.db.get_year(),
            week_day = self.db.get_week_day()
        )

    def save(self, calendar: Calendar):
        self.db.set_day(calendar.day)
        self.db.set_month(calendar.month)
        self.db.set_year(calendar.year)
        self.db.set_week_day(calendar.week_day)
        self.db.set_ship(calendar.can_ship())
        self.logger.info(self.filename, "Nuova data salvata nel database")