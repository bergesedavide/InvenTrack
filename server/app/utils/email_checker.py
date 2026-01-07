

def check_email(email: str):
    if not "@" in email:
        return {"message": "Email non contenente '@'"}, 400
    
    username = email.split("@")[0]
    domain = email.split("@")[1]

    if not username or domain:
        return {"message": "Manca l'username o il dominio"}, 400
    
    return {"username": username, "domain": domain, "message": "Email controllata"}, 200