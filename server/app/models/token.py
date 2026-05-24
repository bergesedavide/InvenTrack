class Token:
    def __init__(self, email: str, token: str, created_at: str):
        self.email = email
        self.token = token
        self.created_at = created_at