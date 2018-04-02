from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .models import Kindergarten
from users.models import User
from django.http import Http404
# Create your views here.

# todo: a detailView and a ListView with paging
import urllib.request
import json
import re

def advanced_search(request):
	if request.method == 'GET':
		return render(request, 'advaned.html')
	if request.method == 'POST':
		p_school = request.POST.get('school_key')
		target = fuzzy_filter(p_school, Kindergarten.objects.all())
		return render(request, 'advaned.html', {'user_list': target})


def guided_search(request):
	if request.method == 'GET':
		return render(request, 'search_by_guidance.html')
	if request.method == 'POST':
		p_sg = request.POST.get('singaporean_key')
		p_certificate = request.POST.get('certificate_key')
		p_year = request.POST.get('year_old_key')
		p_post = request.POST.get('post_key')
		p_dis = request.POST.get('distance_key')
		p_price = request.POST.get('price_key')
		p_second = request.POST.get('second_language_key')
		kindergarten = Kindergarten.objects.all()

		k2 = False
		if p_sg.upper() == 'YES' or p_sg.upper == 'Y':
			kindergarten = selecetMOE(kindergarten)
		if int(p_year) <= 6 or int(p_year) >= 5:
			k2 = True
		kindergarten = year_kindergarten(k2, kindergarten)
		if p_certificate.upper() == 'YES' or p_certificate.upper() == 'Y':
			kindergarten = selecetSPARK(kindergarten)
		kindergarten = price_select(str(p_price), kindergarten, k2)
		kindergarten = language_select(p_second, kindergarten)
		print(kindergarten)
		return render(request, 'search_by_guidance.html', {'user_list': kindergarten})


def language_select(p_second, collection):
	if p_second == 'cn':
		target_kind = collection.filter(language='Chinese')
	if p_second == 'my':
		target_kind = collection.filter(language='Malay')
	if p_second == 'tm':
		target_kind = collection.filter(language='Tamil')
	return target_kind


def price_select(price, collection, k2):
	# todo
	int_p = int(price)
	if int_p == 1000:
		if k2:
			target_kind = collection.filter(k2fee__lte=1000)
		else:
			target_kind = collection.filter(k1fee__lte=1000)
	elif int_p == 1500:
		if k2:
			target_kind = collection.filter(k2fee__gte=1000, k2_fee__lte=1500)
		else:
			target_kind = collection.filter(k1fee__gte=1000, k1_fee__lte=1500)
	elif int_p == 2000:
		if k2:
			target_kind = collection.filter(k2fee__gte=1500, k2_fee__lte=2000)
		else:
			target_kind = collection.filter(k1fee__gte=1500, k1_fee__lte=2000)
	elif int_p == 2500:
		if k2:
			target_kind = collection.filter(k2fee__gte=2000, k2_fee__lte=2500)
		else:
			target_kind = collection.filter(k1fee__gte=2000, k1_fee__lte=2500)
	elif int_p == 3000:
		if k2:
			target_kind = collection.filter(k2fee__gte=2500, k2_fee__lte=3000)
		else:
			target_kind = collection.filter(k1fee__gte=2500, k1_fee__lte=3000)
	else:
		if k2:
			target_kind = collection.filter(k2fee__gte=3000)
		else:
			target_kind = collection.filter(k1fee__gte=3000)
	# if k2:
	#     target_kind = collection.filter(k2fee__gte=lower, k2fee__lte=upper)
	# else:
	#     target_kind = collection.filter(k1fee__gte=lower, k1fee__lte=upper)
	return target_kind


def selecetMOE(collection):
	# target_kind = collection.filter(MOE == True)
	target_kind = collection.filter(type='MOE')
	return target_kind


def selecetSPARK(collection):
	target_kind = collection.filter(sparkCer=True)
	return target_kind


def year_kindergarten(K2, collection):
	# target_kind = []
	# if K2:
	#     for i in collection:
	#         if collection.K2_capacity > 0:
	#             target_kind.insert(i)
	# else:
	#     for i in collection:
	#         if collection.K1_capacity > 0:
	#             target_kind.insert(i)
	# return target_kind
	if K2:
		target_kind = collection.filter(k2_capacity__gt=0)
	else:
		target_kind = collection.filter(k1_capacity__gt=0)
	return target_kind


def distant_selection(target_distant, zip, collection):
	target_kind = collection.filter(calculatedistance(Kindergarten.postalcode, zip) < target_distant)
	return target_kind


def calculatedistance(zip_home, zip_school):
	query = "https://maps.googleapis.com/maps/api/directions/json?origin=home&destination=school&region=sg&key=AIzaSyALTRUtyRv0xcAxEj1mJklVHHXnU77OVE4"
	query = query.replace("home", str(zip_home))
	query = query.replace("school", str(zip_school))
	with urllib.request.urlopen(query) as url:
		data = json.loads(url.read().decode())
		dist = data['routes'][0]['legs'][0]['distance']['value']
		return dist


def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)


def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)


def fuzzy_filter(user_input, collection):
	suggestions = []
	pattern = '.*'.join(user_input)
	regex = re.compile(pattern)
	for item in collection:
		match = regex.search(item)
		if match:
			suggestions.append(item)
	return suggestions


class SchoolListView(View):
	def get(self, request):
		kindergarten_list = Kindergarten.objects.all()
		page = request.GET.get('page', 1)
		
		paginator = Paginator(kindergarten_list, 10)
		try:
			kindergarten = paginator.page(page)
		except PageNotAnInteger:
			kindergarten = paginator.page(1)
		except EmptyPage:
			kindergarten = paginator.page(paginator.num_pages)

		return render(request, 'school_page.html', {'kindergarten': kindergarten})


class SchoolDetailView(View):
	def get(self, request, pk):
		try:
			school = Kindergarten.objects.get(pk=pk)
		except Kindergarten.DoesNotExist:
			raise Http404("Kindergarten does not exists")
		
		context = {'school': school}
		return render(request, 'school_detail.html', context)


def saveToList(request, pk):
	try:
		user = User.objects.get(username=request.session['member_id'])
	except:
		# print('here')
		return render(request, 'login.html')
	school = Kindergarten.objects.get(id=pk)
	if school in user.following.all():
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	else:
		user.following.add(school)
		user.save()
		# print('ok')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def deleteFromList(request, pk):
	try:
		user = User.objects.get(username=request.session['member_id'])
	except:
		# print('here')
		return render(request, 'login.html')
	school = Kindergarten.objects.get(id=pk)
	if school in user.following.all():
		user.following.remove(school)
		user.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
