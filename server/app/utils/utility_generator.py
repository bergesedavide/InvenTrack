import secrets
import string

# Creazione di un generatore di token univoco
def generate_token(email: str, length: int = 32):
    if length < 24:
        return {"message": "Lunghezza troppo corta, rischio attacco hacker"}
    
    alphabets = string.ascii_letters + string.digits
    token = "".join(secrets.choice(alphabets) for _ in range(length))

    # Controllare che il token non esista già
    if token in []:
        generate_token()
    else:
        # Aggiungere il token alla lista di quelli in uso
        pass

    return token

# Creazione di una password sicura
def generate_password(length: int = 16):
    if length < 8:
        return {"message": "Lunghezza troppo corta, rischio attacco hacker"}
    
    alphabets = string.ascii_letters + string.digits + '!@#$%&*_-?'
    password = "".join(secrets.choice(alphabets) for _ in range(length))
    return password

# Controllore di efficienza password
def check_password_strength(password: str):
    pass

