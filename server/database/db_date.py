from server.database.db_conn import get_supabase_client

db = get_supabase_client()

# Get
def get_day() -> int:
    response = db.table("calendar").select("day").execute()
    day = response.data[0]['day']
    day = int(day)
    return day

def get_month() -> int:
    response = db.table("calendar").select("month").execute()
    month = response.data[0]['month']
    month = int(month)
    return month

def get_year() -> int:
    response = db.table("calendar").select("year").execute()
    year = response.data[0]['year']
    year = int(year)
    return year

def get_leap_year() -> int:
    response = db.table("calendar").select("next_leap_year").execute()
    next_leap_year = response.data[0]['next_leap_year']
    next_leap_year = int(next_leap_year)
    return next_leap_year

def get_week_day() -> int:
    response = db.table("calendar").select("week_day").execute()
    week_day = response.data[0]['week_day']
    week_day = int(week_day)
    return week_day

# Update
def set_day(day: int):
    db.table("calendar").update({"day": day}).eq("id", 1).execute()

def set_month(month: int):
    db.table("calendar").update({"month": month}).eq("id", 1).execute()

def set_year(year: int):
    db.table("calendar").update({"year": year}).eq("id", 1).execute()

def set_leap_year(leap_year: int):
    db.table("calendar").update({"next_leap_year": leap_year}).eq("id", 1).execute()

def set_week_day(week_day: int):
    db.table("calendar").update({"week_day": week_day}).eq("id", 1).execute()
