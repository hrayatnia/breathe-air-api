from .Response import ResponseError
import json
from uuid import uuid4
from datetime import datetime
from ..helper.time_tostamp import to_timestamp

class AllStationResponse:
    uuid = None
    date = None
    error = None
    data = None

    def __init__(self,data):
        self.uuid = str(uuid4())
        self.date = to_timestamp(str(datetime.now()))
        self.error = None
        self.data = list(map(lambda x: StationData(x), data))


    def toJSON(self):
        return json.dumps(self.__dict__)

class StationData:
    lat = None
    lon = None
    uid = None
    AQI = None
    name = None

    def __init__(self,data):
        self.lat = data["lat"]
        self.lon = data["lon"]
        self.uid = data["uid"]
        self.AQI = data["aqi"]
        self.name = data["station"]["name"]