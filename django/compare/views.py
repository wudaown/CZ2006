from django.shortcuts import render
from django.http import HttpResponse
from users.models import CompareList
from users.models import User
from schools.models import Kindergarten


def add(request):
	try:
		u = User.objects.get(username=request.session['member_id'])
	except:
		return render(request, 'login.html')

	if len(CompareList.objects.filter(user=u))>3:
		return render(request, 'compare_modify.html', {'msg':
		'Cannot add to compare because there are already 3 schools in compare.'})

	try:
		s = request.POST.get('kindergarten_key') # TODO
		relation = CompareList(user=u, school=s)
		relation.save()
		return render(request, 'compare_modify.html', {'msg': 'Add to compare list succeeded.'})
	except:
		return render(request, 'compare_modify.html', {'msg': 'Add to compare list failed.'})


def remove(request):
	try:
		u = User.objects.get(username=request.session['member_id'])
	except:
		return render(request, 'login.html')

	s = request.POST.get('kindergarten_key') # TODO
	CompareList.objects.filter(user=u, school=s).delete()
	return render(request, 'compare_modify.html', {'msg': '%s deleted from %s\'s compare list'.format(s, u)})

def remove_all(request):
	try:
		u = User.objects.get(username=request.session['member_id'])
	except:
		return render(request, 'login.html')

	CompareList.objects.filter(user=u).delete()
	return render(request, 'compare_modify.html', {'msg': 'All schools deleted from %s\'s compare list'.format(u)})

def result(request, order_by='price'):
	try:
		u = User.objects.get(username=request.session['member_id'])
	except:
		return render(request, 'login.html')

	compareList = CompareList.objects.order_by(order_by).filter(user=u)
	return render(request, 'compare.html', {'user_list': compareList})
