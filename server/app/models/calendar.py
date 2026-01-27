
class Calendar:
    MONTHS = {
        1: "GENNAIO", 2: "FEBBRAIO", 3: "MARZO", 4: "APRILE",
        5: "MAGGIO", 6: "GIUGNO", 7: "LUGLIO", 8: "AGOSTO",
        9: "SETTEMBRE", 10: "OTTOBRE", 11: "NOVEMBRE", 12: "DICEMBRE"
    }

    LONG_MONTHS = {"GENNAIO", "MARZO", "MAGGIO", "LUGLIO", "AGOSTO", "OTTOBRE", "DICEMBRE"}
    SHORT_MONTHS = {"APRILE", "GIUGNO", "SETTEMBRE", "NOVEMBRE"}

    WEEK_DAYS = {
        1: "LUNEDI", 2: "MARTEDI", 3: "MERCOLEDI",
        4: "GIOVEDI", 5: "VENERDI", 6: "SABATO", 7: "DOMENICA"
    }

    WORKING_DAYS = {"LUNEDI", "MARTEDI", "MERCOLEDI", "GIOVEDI", "VENERDI"}

    def __init__(self, day, month, year, week_day):
        self.day = day
        self.month = month
        self.year = year
        self.week_day = week_day

    def is_leap_year(self):
        return self.year % 4 == 0
    
    def days_in_month(self):
        month_name = self.MONTHS[self.month]
        if month_name in self.LONG_MONTHS:
            return 31
        if month_name in self.SHORT_MONTHS:
            return 30
        return 29 if self.is_leap_year() else 28
    
    def advance_day(self):
        self.day += 1
        self.week_day = 1 if self.week_day == 7 else self.week_day + 1

        if self.day > self.days_in_month():
            self.day = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1

    def can_ship(self):
        return self.WEEK_DAYS[self.week_day] in self.WORKING_DAYS