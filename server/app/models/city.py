

class City:
    def __init__(self, desc: str, idState: int, cap: str, lat: str, lon: str):
        self.desc = desc
        self.idState = idState
        self.cap = cap
        self.lat = lat
        self.lon = lon


class State:
    def __init__(self, desc):
        self.desc = desc