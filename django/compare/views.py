from django.shortcuts import render
from django.http import HttpResponse
from users.models import CompareList
from users.models import User
from schools.models import Kindergarten


def add(request, u, s):
	if type(u) == User and type(s) == Kindergarten and u and s:  # not blank
		relation = CompareList(user=u, school=s)
		relation.save()
		return HttpResponse('add to compare list succeeded.')
	else:
		return HttpResponse('add to compare list failed.')


def remove(request, u, s):
	CompareList.objects.filter(user=u, school=s).delete()
	return HttpResponse("%s deleted from %s's compare list".format(s, u))


def result(request, u, order_by='data'):
	compareList = CompareList.objects.order_by(order_by).filter(user=u)
	return render(request, 'compare.html', context=compareList)
