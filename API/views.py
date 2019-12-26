from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .data.MockDataResponse import DATA
from .data.Coordinate import Coordinate
from .AQIcn.AQIAPI import AQIAPI
from .data.Response import AQIResponse,Encoder
# Create your views here.

@csrf_exempt
def location_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        lat = data.get("lat",-33.6892)
        lon = data.get("long",51.3890)
        coord = Coordinate(lat=lat,lng= lon)
        data = AQIAPI().get_by_coordinate(coord=coord)
        data = AQIResponse(data["data"])
        data = Encoder().encode(data)
        return HttpResponse(data,status=200,content_type='application/json')
    return HttpResponse("method not allowed",status=405)
