import aqicn

class AQIAPI:
    API = None
    def __init__(self):
        self.API = aqicn.AqicnApi(secret="a9cde2baacd93d92cddb54a4df55a8d7b12dc938")


    def get_by_coordinate(self,coord):
        return  self.API.get_location_feed(coord=coord)