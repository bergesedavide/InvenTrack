from db_conn import get_supabase_client

db = get_supabase_client()

# CRUD

# Create
def insert_branch(branc):
    response = db.schema("public").table("branches").insert(branc).execute()
    print(response.data)

def insert_discount(discount):
    response = db.schema("public").table("discount").insert(discount).execute()
    print(response.data)

# Read
def get_branches():
    response = db.schema("public").table("branches").select("*").execute()
    print(response.data)

# Update

# Delete