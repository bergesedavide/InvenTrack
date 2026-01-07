from app.database.database_connection import get_supabase_client

class CalendarOperation:
    def __init__(self):
        self.db = get_supabase_client()

    # Get
    def get_day(self) -> int:
        response = self.db.table("calendar").select("day").execute()
        day = response.data[0]['day']
        day = int(day)
        return day

    def get_month(self) -> int:
        response = self.db.table("calendar").select("month").execute()
        month = response.data[0]['month']
        month = int(month)
        return month

    def get_year(self) -> int:
        response = self.db.table("calendar").select("year").execute()
        year = response.data[0]['year']
        year = int(year)
        return year

    def get_week_day(self) -> int:
        response = self.db.table("calendar").select("week_day").execute()
        week_day = response.data[0]['week_day']
        week_day = int(week_day)
        return week_day

    def get_ship(self) -> bool:
        response = self.db.table("calendar").select("shipping").execute()
        ship = response.data[0]['shipping']
        ship = int(ship)
        return ship

    # Update
    def set_day(self, day: int):
        self.db.table("calendar").update({"day": day}).eq("id", 1).execute()

    def set_month(self, month: int):
        self.db.table("calendar").update({"month": month}).eq("id", 1).execute()

    def set_year(self, year: int):
        year = str(year)
        self.db.table("calendar").update({"year": year}).eq("id", 1).execute()

    def set_week_day(self, week_day: int):
        self.db.table("calendar").update({"week_day": week_day}).eq("id", 1).execute()

    def set_ship(self, ship: bool):
        self.db.table("calendar").update({"shipping": ship}).eq("id", 1).execute()