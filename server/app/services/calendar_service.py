from app.database.calendar_repository import CalendarRepository
from app.services.logger_service import LoggerService
from app.config import LogFile

from datetime import datetime

class CalendarService:
    def __init__(self):
        self.repo = CalendarRepository()
        self.filename = LogFile.CALENDAR.value
        self.logger = LoggerService()

    def get_date(self):
        cal = self.repo.load()
        return f"{cal.day:02}-{cal.month:02}-{cal.year:04}"

    def get_full_date(self):
        cal = self.repo.load()
        return f"{cal.WEEK_DAYS[cal.week_day]} {cal.day:02}-{cal.month:02}-{cal.year:04}"
    
    def can_ship(self):
        cal = self.repo.load()
        return cal.can_ship()
    
    def change_style_calendar(self, calendar: str) -> str:
        parts = calendar.split("-")
        if len(parts) != 3:
            return calendar
        
        day, month, year = parts
        return f"{year:04}-{month:02}-{day:02}"

    def advance_calendar(self):
        cal = self.repo.load()
        cal.advance_day()
        self.repo.save(cal)
        self.logger.info(self.filename, f"Nuova data: {cal.day:02}-{cal.month:02}-{cal.year:04}", datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
        return {
            "day": cal.day,
            "month": cal.month,
            "year": cal.year,
            "shipping": cal.can_ship()
        }

