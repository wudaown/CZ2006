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
		return render(request, 'search_by_details.html')
	if request.method == 'POST':
		p_sg = request.POST.get('citizenship')
		print(p_sg)
		p_certificate = request.POST.get('SPARK')
		print(p_certificate)
		p_year = request.POST.get('age')
		print(p_year)
		p_post = request.POST.get('adr')
		print(p_post)
		p_dis = request.POST.get('distance')
		print(p_dis)
		p_price = request.POST.get('fee')
		print(p_price)
		p_second = request.POST.get('language')
		print(p_second)
		if p_second == 'ch':
			print(1)
		kindergarten = Kindergarten.objects.all()

		k2 = False
		if p_sg.upper() == 'SINGAPOREAN' or p_sg.upper == 'S':
			kindergarten = selecetMOE(kindergarten)
		if int(p_year) <= 6 or int(p_year) >= 5:
			k2 = True
		kindergarten = year_kindergarten(k2, kindergarten)
		if p_certificate.upper() == 'YES' or p_certificate.upper() == 'Y':
			kindergarten = selecetSPARK(kindergarten)
		kindergarten = price_select(str(p_price), kindergarten, k2)
		# kindergarten = language_select(p_second, kindergarten)
		# kindergarten = distant_selection(p_dis, p_post,kindergarten)
		# # print(kindergarten)
		# # # return render(request, 'search_by_details.html', {'user_list': kindergarten})
		return render(request, 'school_page.html', {'kindergarten': kindergarten})
		# return render(request, 'search_by_details.html')
def distant_selection(target_distant, zip, collection):
	target_kind = []
	for i in collection:
		cal = calculatedistance(i.postalcode, zip)
		if cal < target_distant:
			target_kind.append(i)
	return target_kind
	# target_kind = collection.filter(calculatedistance(Kindergarten.postalcode, zip) < target_distant)
	# return target_kind

def selecetMOE(collection):
	# target_kind = collection.filter(MOE == True)
	target_kind = collection.filter(type='MOE')
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


def price_select(price, collection, k2):
	a = [200, 300, 400, 500, 600]
	if len(price) == 4:
		# if k2:
		# 	target_kind = collection.filter(k2fee__gte=600)
		# else:
		target_kind = only_da_dollar(collection, 600, k2)
	elif int(price) == 150:
		# if k2:
		# 	target_kind = collection.filter(k2fee__lte=150)
		# else:
		target_kind = only_xiao_dollar(collection, 150, k2)
	else:
		for i in range(0, 4):
			if a[i] == int(price):
				break
		if i == 0:
			det = 50
		else:
			det = 100
		# if k2:
		target_kind = dollar(collection, a[i] - det, a[i], k2)
		# else:
		# 	target_kind = dollar(collection, a[i] - det, a[i], k2)
	return target_kind

def dollar(collection, upper, lower, k2):
	target = []
	if k2:
		for i in collection:
			stro = i.k2fee
			strn = stro.replace(',', '')
			price = int(float(strn[1:]))
			if price < upper and lower <= price:
				target.append(i)
	else:
		for i in collection:
			stro = i.k1fee
			strn = stro.replace(',', '')
			price = int(float(strn[1:]))
			if price < upper and lower <= price:
				target.append(i)
	return target
def only_da_dollar(collection, lower, k2):
	target = []
	if k2:
		for i in collection:
			stro = i.k2fee
			strn = stro.replace(',', '')
			price = int(float(strn[1:]))
			if lower <= price:
				target.append(i)
	else:
		for i in collection:
			stro = i.k1fee
			strn = stro.replace(',', '')
			price = int(float(strn[1:]))
			if lower <= price:
				target.append(i)
	return target
def only_xiao_dollar(collection, upper, k2):
	target = []
	if k2:
		for i in collection:
			stro = i.k2fee
			strn = stro.replace(',', '')
			price = int(float(strn[1:]))
			if upper > price:
				target.append(i)
	else:
		for i in collection:
			stro = i.k1fee
			strn = stro.replace(',', '')
			price = int(float(strn[1:]))
			if upper > price:
				target.append(i)
	return target

	# elif int_p == 200:
	# 	if k2:
	# 		target_kind = collection.filter(k2fee__gte=1000, k2_fee__lte=1500)
	# 	else:
	# 		target_kind = collection.filter(k1fee__gte=1000, k1_fee__lte=1500)
	# elif int_p == 2000:
	# 	if k2:
	# 		target_kind = collection.filter(k2fee__gte=1500, k2_fee__lte=2000)
	# 	else:
	# 		target_kind = collection.filter(k1fee__gte=1500, k1_fee__lte=2000)
	# elif int_p == 2500:
	# 	if k2:
	# 		target_kind = collection.filter(k2fee__gte=2000, k2_fee__lte=2500)
	# 	else:
	# 		target_kind = collection.filter(k1fee__gte=2000, k1_fee__lte=2500)
	# elif int_p == 3000:
	# 	if k2:
	# 		target_kind = collection.filter(k2fee__gte=2500, k2_fee__lte=3000)
	# 	else:
	# 		target_kind = collection.filter(k1fee__gte=2500, k1_fee__lte=3000)
	# else:
	# 	if k2:
	# 		target_kind = collection.filter(k2fee__gte=3000)
	# 	else:
	# 		target_kind = collection.filter(k1fee__gte=3000)
	# # if k2:
	# #     target_kind = collection.filter(k2fee__gte=lower, k2fee__lte=upper)
	# # else:
	# #     target_kind = collection.filter(k1fee__gte=lower, k1fee__lte=upper)
	# return target_kind
def language_select(p_second, collection):
	target_kind = collection
	if p_second == 'cn':
		target_kind = collection.filter(language='Chinese')
	if p_second == 'my':
		target_kind = collection.filter(language='Malay')
	if p_second == 'tm':
		target_kind = collection.filter(language='Tamil')
	return target_kind


def selecetSPARK(collection):
	target_kind = collection.filter(sparkCer=True)
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
