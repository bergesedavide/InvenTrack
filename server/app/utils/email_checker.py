import string

# controlli tutti superflui essendo un login, controllare più che altro se ha senso checkare una email
"""
def check_email(email: str):    
    count = 0
    for c in email:
        if c == "@":
            count += 1

        if count > 1:
            return {"message": "Email contenente più di un '@'"}, 400
        
        if c in string.punctuation:
            return {"message": "Email contenente un segno di punteggiatura. Non valido!"}, 400
        
    if count == 0:
       return {"message": "Email non contenente '@'"}, 400     
    
    username = email.split("@")[0]
    domain = email.split("@")[1]

    if not username or domain:
        return {"message": "Manca l'username o il dominio"}, 400
    
    return {"username": username, "domain": domain, "message": "Email controllata"}, 200
"""