import aqicn
from ..data.Coordinate import Coordinate
class AQIAPI:
    API = None
    def __init__(self):
        self.API = aqicn.AqicnApi(secret="a9cde2baacd93d92cddb54a4df55a8d7b12dc938")


    def get_by_coordinate(self,coord):
        return  self.API.get_location_feed(coord=coord)

    def get_all(self):
        return self.API.get_stations_in_area(lower_left=Coordinate(lat=-80,lng=-180.),upper_right=Coordinate(lat=80,lng=180.))

    def search_by_name(self,name):
        return self.API.search(name)

    def get_by_name(self,name):
        return self.API.get_feed(name)