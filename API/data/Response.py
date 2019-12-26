from json import JSONEncoder
from uuid import uuid4
from datetime import datetime
from ..helper.time_tostamp import to_timestamp
import json
class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class AQIResponse:
    uuid = None
    date = None
    error = None
    data = None
    location = None
    offerToDo = None

    def __init__(self,data):
        self.uuid = str(uuid4())
        self.date = to_timestamp(str(datetime.now()))
        self.error = None
        self.location = Location(data["city"])
        self.offerToDo = [OfferTodo()]
        self.data = ResponseData(data["aqi"],data["iaqi"])

    def toJSON(self):
        return json.dumps(self.__dict__)


class ResponseError:
    message = None
    code = None
    localeMessage = None


class Location:
    lat = None
    lon = None
    name = None

    def __init__(self,city):
        self.lat = city["geo"][0]
        self.lon = city["geo"][1]
        self.name =city["name"].split(",")[1]

class ResponseData:
    AQIIndex = None
    pm2 = None
    pm10 = None
    co2 = None
    others = None

    def __init__(self,AQI,iaqi):
        self.AQIIndex = AQI
        self.pm2 = iaqi.get('pm25',{'v':0})['v']
        self.pm10 = iaqi.get('pm10',{'v':0})['v']
        self.co2 = iaqi.get('co',{'v':0})['v']
        self.others = []
        print()

class OfferTodo:
    imageUrl = None
    text = None

    def __init__(self):
        self.text = ""
        self.imageUrl = ""