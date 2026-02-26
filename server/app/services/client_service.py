from app.models.client import Client
from app.models.city import City
from app.database.state_repository import StateRepository
from app.database.city_repository import CityRepository
from app.database.gender_repository import GenderRepository
from app.database.client_repository import ClientRepository
from app.services.calendar_service import CalendarService
from app.utils.utility_generator import replace_domain, generate_card, generate_password

import requests

class ClientService:
    def __init__(self):
        self.baseUrl = "https://randomuser.me/api/?nat=us&inc=gender,name,location,email,dob&results="
        self.stateRepo = StateRepository()
        self.cityRepo = CityRepository()
        self.clientRepo = ClientRepository()
        self.cal = CalendarService()
        self.gender = GenderRepository()

    def add_client(self, num: int = 1):
        url = self.baseUrl + str(num)

        res = requests.get(url)

        if res.status_code != 200:
            return {"message": "Errore nella richiesta di scaricamento utente", "cod": 400}
        
        res = res.json()

        for result in res["results"]:
            gender = result["gender"]
            codGender = self.gender.get_gender_by_desc_eng(gender)

            result_name = result["name"]
            name = result_name["first"]
            surname = result_name["last"]

            result_location = result["location"]
            address = result_location["street"]["name"]
            numAddress = result_location["street"]["number"]

            city_desc = result_location["city"]
            state = result_location["state"]
            cap = result_location["postcode"]
            lat = result_location["coordinates"]["latitude"]
            lon = result_location["coordinates"]["longitude"]

            idState = self.stateRepo.get_id_by_desc(state.lower())

            city = City(city_desc, idState, cap, lat, lon)
            idCity = self.cityRepo.get_id_by_desc(city)

            email = result["email"]
            email = replace_domain(email)

            card = generate_card()

            dob = result["dob"]["date"]
            dob = dob.split("T")[0]

            dateReg = self.cal.get_date()
            dateReg = self.cal.change_style_calendar(dateReg)

            pwd = generate_password()

            client = Client(name, surname, email, pwd, dob, card, idCity, codGender, address, numAddress, dateReg)
            
            self.clientRepo.save(client)

    def get_client_by_id(self, idClient: int) -> Client:
        return self.clientRepo.get_client_by_id(idClient)