from django.shortcuts import render
from django.http import HttpResponse
from .models import School

# Create your views here.

#todo: a detailView and a ListView with paging
def school_info(request, centre_code):
	school = School.object.all()

	return HttpResponse("You are look at school %s.".format(name))

