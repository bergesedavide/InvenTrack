import threading
from datetime import datetime
from app.services.calendar_service import CalendarService
from app.services.logger_service import LoggerService
from app.config import LogFile

class CalendarScheduler:
    def __init__(self, interval_minutes=10):
        self.interval = interval_minutes * 60
        self.service = CalendarService()
        self._running = False
        self._timer = None
        self.logger = LoggerService()
        self.filename = LogFile.CALENDAR.value

    def start(self):
        if self._running:
            self.logger.warning(self.filename, f"Avanzamento automatico gia attivo", datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
            return

        self._running = True

        def _tick():
            if not self._running:
                self.logger.warning(self.filename, f"Avanzamento automatico non attivo", datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
                return

            self.service.advance_calendar()

            self._timer = threading.Timer(self.interval, _tick)
            self._timer.start()

        self._timer = threading.Timer(self.interval, _tick)
        self._timer.start()
        self.logger.info(self.filename, f"Avanzamento automatico iniziato", datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()
            self.logger.info(self.filename, f"Avanzamento automatico terminato", datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
