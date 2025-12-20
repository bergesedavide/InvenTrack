import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "date.json")

def read_calendar():
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    
def write_calendar(data: dict):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# GET
def get_day() -> int:
    return int(read_calendar()["day"])

def get_month() -> int:
    return int(read_calendar()["month"])

def get_year() -> int:
    return int(read_calendar()["year"])

def get_leap_year() -> int:
    return int(read_calendar()["next_leap_year"])

def get_week_day() -> int:
    return int(read_calendar()["week_day"])


# PUT
def set_day(day: str) -> str:
    date = read_calendar()
    date["day"] = day
    write_calendar(date)

def set_month(month: str) -> str:
    date = read_calendar()
    date["month"] = month
    write_calendar(date)

def set_year(year: str) -> str:
    date = read_calendar()
    date["year"] = year
    write_calendar(date)

def set_leap_year(leap_year: str) -> str:
    date = read_calendar()
    date["next_leap_year"] = leap_year
    write_calendar(date)

def set_week_day(week_day: str) -> str:
    date = read_calendar()
    date["week_day"] = week_day
    write_calendar(date)