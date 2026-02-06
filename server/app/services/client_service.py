from app.models.client import Client

import requests

class ClientService:
    def __init__(self):
        self.baseUrl = "https://randomuser.me/api/?nat=us&inc=gender,name,location,email,login&results="

    def add_client(self, num: int = 1):
        url = self.baseUrl + str(num)

        res = requests.get(url)

        if res.status_code != 200:
            return {"message": "Errore nella richiesta di scaricamento utente", "cod": 400}
        
        res = res.json()

        for result in res["results"]:
            gender = result["gender"]

            result_name = result["name"]
            name = result_name["first"]
            surname = result_name["last"]

            result_location = result["location"]
            address = result_location["street"]["name"]
            numAddress = result_location["street"]["number"]

            city = result_location["city"]          #TODO: estrapola l'id e si aggiungono le info nella tabella città 
            state = result_location["state"]
            cap = result_location["postCode"]
            lat = result_location["coordinates"]["latitude"]
            lon = result_location["coordinates"]["longitude"]

            email = result["email"]        #TODO: chiamare metodo per modificare il dominio della email
            username = result["login"]["username"]
            print(result)
        return res