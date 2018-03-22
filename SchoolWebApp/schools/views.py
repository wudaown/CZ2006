from django.shortcuts import render
from django.http import HttpResponse
from .models import School

# Create your views here.


def school_info(request, centre_code):
	school = School.object.filter(centre_code=centre_code)
	name = school.centre_name
	return HttpResponse("You are look at school %s.".format(name))

