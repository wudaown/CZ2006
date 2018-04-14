from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .models import Kindergarten, Language
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


# TODO
# need to consult UI to finalise form
class GuideSearch(View):
	def get(self, request):
		return render(request, 'search_by_details.html')
	
	def post(self, request):
		all_k = Kindergarten.objects.all()
		
		all_k = self.getFee(request, all_k)
		
		all_k = self.getMis(request, all_k)
		
		all_k = self.getLangType(request, all_k)
		
		context = self.getDis(request, all_k)
		
		# TODO
		# pagination to be done
		# print()
		return render(request, 'search_by_details.html', context)
	
	def getMis(self, request, all_k):
		spark = bool(request.POST.get('spark'))
		bus = bool(request.POST.get('bus'))
		outdoor = bool(request.POST.get('outdoor'))
		if spark:
			all_k = all_k.filter(sparkCer=bool(request.POST.get('spark')))
		if bus:
			all_k = all_k.filter(bus=bool(request.POST.get('bus')))
		if outdoor:
			all_k = all_k.filter(outdoor=bool(request.POST.get('outdoor')))
		return all_k
	
	def getLangType(self, request, all_k):
		all_lang = Language.objects.all()
		type_k = []
		type_list = []
		# TODO
		# html my-box class value attribute color
		type_k.append(request.POST.get('commercial'))
		type_k.append(request.POST.get('moe'))
		type_k.append(request.POST.get('aop'))
		type_k.append(request.POST.get('pop'))
		type_k.append(request.POST.get('nfp'))
		
		lang_k = []
		lang_list = []
		lang_k.append(request.POST.get('language1'))
		lang_k.append(request.POST.get('language2'))
		lang_k.append(request.POST.get('language3'))
		lang_k.append(request.POST.get('language4'))
		lang_k.append(request.POST.get('language5'))
		for i in type_k:
			if i is not None:
				type_list.append(all_k.filter(type__icontains=i))
		if not all(i is None for i in type_k):
			all_k = Kindergarten.objects.none()
		
		for x in type_list:
			all_k = all_k.union(x)
		
		for i in range(len(lang_k)):
			if lang_k[i] is not None:
				lang_list.append(all_k.filter(language=all_lang[i]))
		if not all(i is None for i in lang_k):
			all_k = Kindergarten.objects.none()
		for x in lang_list:
			all_k = all_k.union(x)
		
		return all_k
	
	def getDis(self, request, all_k):
		zip = int(request.POST.get('zip'))
		min_dis = int(request.POST.get('min-dis'))
		max_dis = int(request.POST.get('max-dis'))
		final_set = []
		if max_dis >= 9999:
			context = {'kindergarten': all_k}
		else:
			for i in all_k:
				dist = self.calculatedistance(zip, i.postalcode)
				if min_dis <= dist <= max_dis:
					final_set.append(i)
			context = {'kindergarten': final_set}
		return context
	
	def getFee(self, request, all_k):
		grade = request.POST.get('programme')
		min_fee = int(request.POST.get('min-fee'))
		max_fee = int(request.POST.get('max-fee'))
		if grade == 'k1':
			all_k = all_k.filter(k1_capacity__gte=0)
			all_k = all_k.filter(k1fee__range=(min_fee, max_fee))
		elif grade == 'k2':
			all_k = all_k.filter(k2_capacity__gte=0)
			all_k = all_k.filter(k1fee__range=(min_fee, max_fee))
		return all_k
	
	def calculatedistance(self, zip_home, zip_school):
		query = "https://maps.googleapis.com/maps/api/directions/json?origin=home&destination=school&region=sg&key=AIzaSyALTRUtyRv0xcAxEj1mJklVHHXnU77OVE4"
		query = query.replace("home", str(zip_home))
		query = query.replace("school", str(zip_school))
		with urllib.request.urlopen(query) as url:
			data = json.loads(url.read().decode())
			if data['status'] == 'ZERO_RESULTS':
				return -1
			else:
				dist = data['routes'][0]['legs'][0]['distance']['value'] / 1000
				return dist


# def guided_search(request):
# 	if request.method == 'GET':
# 		return render(request, 'search_by_details_edit.html')
# 	if request.method == 'POST':
# 		p_sg = request.POST.get('citizenship')
# 		print(p_sg)
# 		p_certificate = request.POST.get('SPARK')
# 		print(p_certificate)
# 		p_year = request.POST.get('age')
# 		print(p_year)
# 		p_post = request.POST.get('adr')
# 		print(p_post)
# 		p_dis = request.POST.get('distance')
# 		print(p_dis)
# 		p_price = request.POST.get('fee')
# 		print(p_price)
# 		p_second = request.POST.get('language')
# 		print(p_second)
# 		# if p_second == 'ch':
# 		# 	print(1)
# 		kindergarten = Kindergarten.objects.all()
#
# 		k2 = False
#         #Todo: Does not handle NULL input [faceplam]
#         #Todo:Not all singaporean must go to moe schools [facepalm], and no moe schools in database so far, only daxiongdi have
# 		if p_sg.upper() == 'SINGAPOREAN' or p_sg.upper == 'S':
# 			kindergarten = selecetMOE(kindergarten)
# 		print(kindergarten)
# 		if int(p_year) <= 6 or int(p_year) >= 5:
# 			k2 = True
# 		kindergarten = year_kindergarten(k2, kindergarten)
# 		if p_certificate.upper() == 'YES' or p_certificate.upper() == 'Y':
# 			kindergarten = selecetSPARK(kindergarten)
# 		print(kindergarten)
# 		kindergarten = price_select(str(p_price), kindergarten, k2)
# 		kindergarten = language_select(p_second, kindergarten)
# 		kindergarten = distant_selection(p_dis, p_post,kindergarten)
# 		# for i in kindergarten:
# 		# 	print(i.name, i.postalcode, i.type, i.email, i.language)
#
# 		print(kindergarten)
# 		# # # return render(request, 'search_by_details.html', {'user_list': kindergarten})
# 		return render(request, 'search_by_details_edit.html', {'kindergarten': kindergarten})
# 		# return render(request, 'search_by_details.html')


# def distant_selection(target_distant, zip, collection):
# 	target_kind = []
# 	a = [2, 5, 10, 15, 20]
# 	if len(target_distant) == 3:
# 		target_kind = collection
# 	else:
# 		for i in range(0, 5):
# 			if a[i] == int(target_distant):
# 				break
# 		for i in collection:
# 			cal = calculatedistance(i.postalcode, zip)
# 			if cal < target_distant:
# 				target_kind.append(i)
# 	return target_kind
# 	# target_kind = collection.filter(calculatedistance(Kindergarten.postalcode, zip) < target_distant)
# 	# return target_kind
#
# def selecetMOE(collection):
# 	# target_kind = collection.filter(MOE == True)
# 	target_kind = collection.filter(type='MOE')
# 	return target_kind
#
#
# def year_kindergarten(K2, collection):
# 	if K2:
# 		target_kind = collection.filter(k2_capacity__gt=0)
# 	else:
# 		target_kind = collection.filter(k1_capacity__gt=0)
# 	return target_kind


# def price_select(price, collection, k2):
# 	a = [200, 300, 400, 500, 600]
# 	if len(price) == 4:
# 		# if k2:
# 		# 	target_kind = collection.filter(k2fee__gte=600)
# 		# else:
# 		target_kind = only_da_dollar(collection, 600, k2)
# 	elif int(price) == 150:
# 		# if k2:
# 		# 	target_kind = collection.filter(k2fee__lte=150)
# 		# else:
# 		target_kind = only_xiao_dollar(collection, 150, k2)
# 	else:
# 		for i in range(0, 5):
# 			if a[i] == int(price):
# 				break
# 		if i == 0:
# 			det = 50
# 		else:
# 			det = 100
# 		# if k2:
# 		target_kind = dollar(collection, a[i] - det, a[i], k2)
# 		# else:
# 		# 	target_kind = dollar(collection, a[i] - det, a[i], k2)
# 	return target_kind
#
# def dollar(collection, upper, lower, k2):
# 	target = []
# 	if k2:
# 		for i in collection:
# 			stro = i.k2fee
# 			strn = stro.replace(',', '')
# 			price = int(float(strn[1:]))
# 			if price < upper and lower <= price:
# 				target.append(i)
# 	else:
# 		for i in collection:
# 			stro = i.k1fee
# 			strn = stro.replace(',', '')
# 			price = int(float(strn[1:]))
# 			if price < upper and lower <= price:
# 				target.append(i)
# 	return target
# def only_da_dollar(collection, lower, k2):
# 	target = []
# 	if k2:
# 		for i in collection:
# 			stro = i.k2fee
# 			strn = stro.replace(',', '')
# 			price = int(float(strn[1:]))
# 			if lower <= price:
# 				target.append(i)
# 	else:
# 		for i in collection:
# 			stro = i.k1fee
# 			strn = stro.replace(',', '')
# 			price = int(float(strn[1:]))
# 			if lower <= price:
# 				target.append(i)
# 	return target
# def only_xiao_dollar(collection, upper, k2):
# 	target = []
# 	if k2:
# 		for i in collection:
# 			stro = i.k2fee
# 			strn = stro.replace(',', '')
# 			price = int(float(strn[1:]))
# 			if upper > price:
# 				target.append(i)
# 	else:
# 		for i in collection:
# 			stro = i.k1fee
# 			strn = stro.replace(',', '')
# 			price = int(float(strn[1:]))
# 			if upper > price:
# 				target.append(i)
# 	return target
#
# 	# elif int_p == 200:
# 	# 	if k2:
# 	# 		target_kind = collection.filter(k2fee__gte=1000, k2_fee__lte=1500)
# 	# 	else:
# 	# 		target_kind = collection.filter(k1fee__gte=1000, k1_fee__lte=1500)
# 	# elif int_p == 2000:
# 	# 	if k2:
# 	# 		target_kind = collection.filter(k2fee__gte=1500, k2_fee__lte=2000)
# 	# 	else:
# 	# 		target_kind = collection.filter(k1fee__gte=1500, k1_fee__lte=2000)
# 	# elif int_p == 2500:
# 	# 	if k2:
# 	# 		target_kind = collection.filter(k2fee__gte=2000, k2_fee__lte=2500)
# 	# 	else:
# 	# 		target_kind = collection.filter(k1fee__gte=2000, k1_fee__lte=2500)
# 	# elif int_p == 3000:
# 	# 	if k2:
# 	# 		target_kind = collection.filter(k2fee__gte=2500, k2_fee__lte=3000)
# 	# 	else:
# 	# 		target_kind = collection.filter(k1fee__gte=2500, k1_fee__lte=3000)
# 	# else:
# 	# 	if k2:
# 	# 		target_kind = collection.filter(k2fee__gte=3000)
# 	# 	else:
# 	# 		target_kind = collection.filter(k1fee__gte=3000)
# 	# # if k2:
# 	# #     target_kind = collection.filter(k2fee__gte=lower, k2fee__lte=upper)
# 	# # else:
# 	# #     target_kind = collection.filter(k1fee__gte=lower, k1fee__lte=upper)
# 	# return target_kind


# def selecetSPARK(collection):
# 	target_kind = collection.filter(sparkCer=True)
# 	return target_kind


# def results(request, question_id):
# 	response = "You're looking at the results of question %s."
# 	return HttpResponse(response % question_id)
#
#
# def vote(request, question_id):
# 	return HttpResponse("You're voting on question %s." % question_id)


def fuzzy_filter(user_input, collection):
	suggestions = []
	pattern = '.*'.join(user_input)
	regex = re.compile(pattern)
	for item in collection:
		match = regex.search(item)
		if match:
			suggestions.append(item)
	return suggestions


# def language_select(self, p_second, collection):
# 	target_kind = []
# 	if p_second == 'cn':
# 		for i in collection:
# 			if 'Chinese' in [str(j) for j in i.language.all()]:
# 				target_kind.append(i)
# 	elif p_second == 'my':
# 		for i in collection:
# 			if 'Malay' in [str(j) for j in i.language.all()]:
# 				target_kind.append(i)
# 	elif p_second == 'tm':
# 		for i in collection:
# 			if 'Tamil' in [str(j) for j in i.language.all()]:
# 				target_kind.append(i)
# 	else:
# 		target_kind = collection
# 	return target_kind

# class SchoolListView(View):
# 	def get(self, request):
# 		kindergarten_list = Kindergarten.objects.all()
# 		page = request.GET.get('page', 1)
#
# 		paginator = Paginator(kindergarten_list, 10)
# 		try:
# 			kindergarten = paginator.page(page)
# 		except PageNotAnInteger:
# 			kindergarten = paginator.page(1)
# 		except EmptyPage:
# 			kindergarten = paginator.page(paginator.num_pages)
#
# 		return render(request, 'school_page.html', {'kindergarten': kindergarten})


class SchoolDetailView(View):
	def get(self, request, pk):
		# TODO
		# way of indicating message read status
		# try:
		# 	refer = (request.META['HTTP_REFERER'])
		# 	if 'notification' in refer:
		# 		pass
		# except:
		# 	pass
		try:
			school = Kindergarten.objects.get(pk=pk)
		except Kindergarten.DoesNotExist:
			raise Http404("Kindergarten does not exists")
		
		lang = school.language.all()
		context = {'school': school,
		           'lang':   lang}
		return render(request, 'school_detail.html', context)


class ToggleFav(View):
	def get(self, request, pk):
		try:
			user = request.user
			if user.is_anonymous:
				return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		except:
			# return render(request, 'index.html')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
		school = Kindergarten.objects.get(id=pk)
		if school in user.following.all():
			user.following.remove(school)
		else:
			user.following.add(school)
		user.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
