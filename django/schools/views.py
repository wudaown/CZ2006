from django.shortcuts import render
from django.http import HttpResponse
from .models import School
import urllib.request
import json


# Create your views here.

def school_info(request, centre_code):
    school = School.object.filter(centre_code=centre_code)
    name = school.centre_name
    return HttpResponse("You are look at school %s.".format(name))


def calculatedistance(zip_home, zip_school):
    query = "https://maps.googleapis.com/maps/api/directions/json?origin=home&destination=school&region=sg&key=AIzaSyALTRUtyRv0xcAxEj1mJklVHHXnU77OVE4"
    query.replace("home", zip_home)
    query.replace("school", zip_school)
    with urllib.request.urlopen(query) as url:
        data = json.loads(url.read().decode())
        dist = data['routes'][0]['legs'][0]['distance']['value']
        return dist
