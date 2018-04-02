from django.shortcuts import render
from django.http import HttpResponse
from users.models import CompareList
from users.models import User
from schools.models import Kindergarten


def add(request):
	u = request.POST.get('user_key')
	s = request.POST.get('kindergarten_key')
	if type(u) == User and type(s) == Kindergarten and u and s:  # not blank
		relation = CompareList(user=u, school=s)
		relation.save()
		return render(request, 'compare_modify.html', {'msg': 'add to compare list succeeded.'})
	else:
		return render(request, 'compare_modify.html', {'msg': 'add to compare list failed.'})


def remove(request):
	u = request.POST.get('user_key')
	s = request.POST.get('kindergarten_key')
	CompareList.objects.filter(user=u, school=s).delete()
	#return render(request, 'compare_modify.html', {'msg': '%s deleted from %s\'s compare list'.format(s, u))


def result(request, order_by='data'):
	u = request.POST.get('user_key')
	compareList = CompareList.objects.order_by(order_by).filter(user=u)
	return render(request, 'compare.html', {'user_list': compareList})
