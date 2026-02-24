from app.database.token_repository import TokenRepository
import secrets, string
from random import random

tokenRepo = TokenRepository()

# Creazione di un generatore di token univoco
def generate_token(email: str, length: int = 32):
    if length < 24:
        return {"message": "Lunghezza troppo corta, rischio attacco hacker"}
    
    alphabets = string.ascii_letters + string.digits
    token = "".join(secrets.choice(alphabets) for _ in range(length))

    tokens = tokenRepo.get_tokens()
    # Controllare che il token non esista già
    if token in tokens:
        print("Token da riaggiornare")
        generate_token(email)
    else:
        tokenRepo.set_token(email, token)

    return token

# Creazione di una password sicura
def generate_password(length: int = 16) -> str:
    if length < 8:
        return {"message": "Lunghezza troppo corta, rischio attacco hacker"}
    
    alphabets = string.ascii_letters + string.digits + '!@#$%&*_-?'
    password = "".join(secrets.choice(alphabets) for _ in range(length))
    return password

# Controllore di efficienza password
def check_password_strength(password: str):
    pass

# Generatore di booleano per decidere se l'utente ha la tessera o no
def generate_card() -> bool:
    rnd = int(random() * 100)

    if rnd <= 70:
        return False
    else:
        return True

# Sostitutore di domini email
def replace_domain(email: str) -> str:
    username = email.split("@")[0]

    domains = ["gmail.com", "outlook.com", "yahoo.com", "icloud.com"]
    rnd = int(random() * 100)

    if rnd <= 62:
        new_domain = domains[0]
    elif rnd <= 84:
        new_domain = domains[1]
    elif rnd <= 93:
        new_domain = domains[2]
    elif rnd <= 100:
        new_domain = domains[3]

    new_email = username + "@" + new_domain
    return new_email