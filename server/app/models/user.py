

class User:

    def __init__(self, email, password, role):
        self.email = email
        self.username = email.split("@")[0]
        self.password = password
        self.role = role