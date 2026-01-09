from app.database.database_connection import get_supabase_client

class UserOperation:
    def __init__(self):
        self.db = get_supabase_client()

    def get_users(self):
        response = self.db.table("users").select("email, password").execute()
        users = []
        
        for user in response.data:
            email = user["email"]
            pwd = user["password"]
            _user = {
                "email": email,
                "password": pwd
            }

            users.append(_user)
        
        print(users)
