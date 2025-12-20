from database.db_date import get_day, get_month, get_year, get_leap_year, get_week_day, set_day, set_month, set_year, set_leap_year, set_week_day

# Variabili globali
LONG_MONTH = ["GENNAIO", "MARZO", "MAGGIO", "LUGLIO", "AGOSTO", "OTTOBRE", "DICEMBRE"]
SHORT_MONTH = ["APRILE", "GIUGNO", "SETTEMBRE", "NOVEMBRE"]

MONTHS = {
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

MAX_MONTHS = len(MONTHS)

WORKING = ["LUNEDÌ", "MARTEDÌ", "MERCOLEDÌ", "GIOVEDÌ", "VENERDÌ"]
HOLIDAYS = ["SABATO", "DOMENICA"]

WEEK_DAYS = {
    1: "LUNEDÌ",
    2: "MARTEDÌ",
    3: "MERCOLEDÌ",
    4: "GIOVEDÌ",
    5: "VENERDÌ",
    6: "SABATO",
    7: "DOMENICA"
}

# Creazione funzioni
def get_calendar() -> str:
    day = get_day()
    month = get_month()
    year = get_year()
    week_day = get_week_day()

    days_number = 29 if year == get_leap_year() else 28
    month_string = MONTHS[month]
    year_int = None
    month_int = None
    day_int = 1
    week_day_string = WEEK_DAYS[week_day]
    ship = None

    if year == get_leap_year() and month >= 3:
        set_leap_year(str(year + 4))

    if month_string in LONG_MONTH:
        days_number = 31
    elif month_string in SHORT_MONTH:
        days_number = 30

    if week_day_string in WORKING:
        ship = True
    elif week_day_string in HOLIDAYS:
        ship = False

    if day > days_number:
        month_int = month + 1
        set_month(str(month_int))
        set_day(str(day_int))

    if month == MAX_MONTHS and day > days_number:
        month_int = 1
        year_int = year + 1
        set_month(str(month_int))
        set_year(str(year_int))

    # print(days_number)

    if isinstance(year_int, int):
        return {"date": f"{week_day_string} {day_int:02} - {month_int:02} - {year_int}", "shipping": ship}

    if isinstance(month_int, int):
       return {"date": f"{week_day_string} {day_int:02} - {month_int:02} - {year}", "shipping": ship}
    
    return {"date": f"{week_day_string} {day:02} - {month:02} - {year}", "shipping": ship}

def add_day() -> str:
    set_day(str(get_day() + 1))

    if get_week_day() < 7:
        set_week_day(str(get_week_day() + 1))
    elif get_week_day() == 7:
        set_week_day("1")

"""
for i in range (100):
    add_day()
    data_corrente = get_calendar()
    print(data_corrente)
"""

add_day()
data_corrente = get_calendar()
print(data_corrente["date"])
if data_corrente["shipping"]:
    print("I pacchetti possono essere consegnati")
else:
    print("I pacchetti non possono essere consegnati")