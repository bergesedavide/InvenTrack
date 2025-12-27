from server.database.db_date import get_day, get_month, get_year, get_leap_year, get_week_day, set_day, set_month, set_year, set_leap_year, set_week_day
import threading, time

class Calendar:
    def __init__(self):
        self.long_month = ["GENNAIO", "MARZO", "MAGGIO", "LUGLIO", "AGOSTO", "OTTOBRE", "DICEMBRE"]
        self.short_month = ["APRILE", "GIUGNO", "SETTEMBRE", "NOVEMBRE"]

        self.months = {
            1: "GENNAIO",
            2: "FEBBRAIO",
            3: "MARZO",
            4: "APRILE",
            5: "MAGGIO",
            6: "GIUGNO",
            7: "LUGLIO",
            8: "AGOSTO",
            9: "SETTEMBRE",
            10: "OTTOBRE",
            11: "NOVEMBRE",
            12: "DICEMBRE"
        }

        self.max_months = len(self.months)

        self.working_day = ["LUNEDÌ", "MARTEDÌ", "MERCOLEDÌ", "GIOVEDÌ", "VENERDÌ"]
        self.holidays = ["SABATO", "DOMENICA"]

        self.week_days = {
            1: "LUNEDÌ",
            2: "MARTEDÌ",
            3: "MERCOLEDÌ",
            4: "GIOVEDÌ",
            5: "VENERDÌ",
            6: "SABATO",
            7: "DOMENICA"
        }

    def create_calendar(self):
        day = get_day()
        month = get_month()
        year = get_year()
        week_day = get_week_day()

        month_string = self.months[month]
        week_day_string = self.week_days[week_day]

        new_day = day
        new_month = month
        new_year = year

        # --------------------
        # GIORNI DEL MESE
        # --------------------
        if month_string in self.long_month:
            days_number = 31
        elif month_string in self.short_month:
            days_number = 30
        else:
            days_number = 29 if year == get_leap_year() else 28

        # --------------------
        # SHIPPING
        # --------------------
        ship = week_day_string in self.working_day

        # --------------------
        # AVANZAMENTO DATA
        # --------------------
        if day > days_number:
            new_day = 1
            new_month += 1

            if new_month > self.max_months:
                new_month = 1
                new_year += 1

        # --------------------
        # AGGIORNAMENTO DB
        # --------------------
        if new_day != day:
            set_day(new_day)

        if new_month != month:
            set_month(new_month)

        if new_year != year:
            set_year(new_year)

        # --------------------
        # ANNO BISESTILE
        # --------------------
        if year == get_leap_year() and month >= 3:
            set_leap_year(year + 4)

        return {
            "week_day": week_day_string,
            "day": new_day,
            "month": new_month,
            "year": new_year,
            "shipping": ship
        }
    
    # --------------------
    # AUTOMAZIONE OGNI N MINUTI
    # --------------------
    def start_auto_advance(self, interval_minutes: int = 10):
        """Avanza il calendario ogni interval_minutes in background"""
        if getattr(self, "_running", False):
            print("[CALENDAR] Auto-advance già attivo")
            return

        self._running = True
        self.last_calendar = None
        interval_seconds = interval_minutes * 60

        def _advance():
            if not self._running:
                return

            print(f"[CALENDAR] Tick alle {time.strftime('%H:%M:%S')}")

            self.add_day()
            calendar = self.create_calendar()

            print(
                f"[CALENDAR] Nuova data → "
                f"{calendar['day']}-{calendar['month']}-{calendar['year']} | "
                f"{calendar['week_day']} | shipping={calendar['shipping']}"
            )

            self._timer = threading.Timer(interval_seconds, _advance)
            self._timer.start()

        print("[CALENDAR] Auto-advance avviato")
        self._timer = threading.Timer(interval_seconds, _advance)
        self._timer.start()

    def stop_auto_advance(self):
        """Ferma l'automazione"""
        if not getattr(self, "_running", False):
            print("[CALENDAR] Auto-advance non attivo")
            return

        self._running = False

        if self._timer:
            self._timer.cancel()
            self._timer = None

        print("[CALENDAR] Auto-advance fermato")

    # --------------------
    # FUNZIONI DI RESTITUZIONE DATE
    # --------------------
    
    def add_day(self):
        set_day(get_day() + 1)

        next_week_day = get_week_day() + 1
        set_week_day(1 if next_week_day > 7 else next_week_day)

    def change_style_calendar(self, calendar: str) -> str:
        parts = calendar.split("-")
        if len(parts) != 3:
            return calendar
        
        day, month, year = parts
        return f"{year}-{month}-{day}"
    
    def get_date(self) -> str:
        calendar = self.create_calendar()
        return f"{calendar['day']}-{calendar['month']}-{calendar['year']}"
        
    def get_full_date(self) -> str:
        calendar = self.create_calendar()
        return f"{calendar['week_day']} {calendar['day']}-{calendar['month']}-{calendar['year']}"
    
    def can_ship(self) -> str:
        calendar = self.create_calendar()
        return calendar['shipping']

# try
calendario = Calendar()
calendario.start_auto_advance(1)
time.sleep(300)
calendario.stop_auto_advance()