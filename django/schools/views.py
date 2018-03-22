from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Kindergarten
from django.shortcuts import render
from django.http import HttpResponse
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


def guild_search(request):
    if request.method == 'GET':
        return render(request, 'table.html')
    # print(request.GET.get('key'))
    # user_list = User.objects.all()
    # print(locals())
    if request.method == 'POST':
        p_sg = request.POST.get('singaporean_key')
        # print(p_sg)
        p_certificate = request.POST.get('certificate_key')
        # print(p_certificate)
        p_year = request.POST.get('year_old_key')
        # print(p_year)
        p_post = request.POST.get('post_key')
        # print(p_post)
        p_dis = request.POST.get('distance_key')
        # print(p_dis)
        p_price = request.POST.get('price_key')
        # print(p_price)
        p_second = request.POST.get('second_language_key')
        # print(p_second)
        kindergarten = Kindergarten.objects.all()
        if p_sg.upper() == 'YES' or p_sg.upper == 'Y':
            kindergarten = selecetMOE(kindergarten)
        if int(p_year) <= 6 or int(p_year) >= 5:
            k2 = True
        # kindergarten.filter(K2_capacity__gte=0)
        kindergarten = year_kindergarten(k2, kindergarten)
        if p_certificate.upper() == 'YES' or p_certificate.upper() == 'Y':
            kindergarten = selecetSPARK(kindergarten)
        # kindergarten = distant_selection(int(p_dis), p_post, kindergarten)
        kindergarten = price_select(str(p_price), kindergarten, k2)
        kindergarten = fuzzy_filter(p_second, kindergarten)
        return render(request, 'table.html', {'user_list':kindergarten})

def price_select(price, collection, k2):
    price1 = int(re.search(r'\d+', price).group())
    price = price.replace(str(price1), '')
    price2 = int(re.search(r'\d+', price).group())
    lower = min(price1, price2)
    upper = max(price1, price2)
    if k2:
        target_kind = collection.filter(k2fee__gte=lower, k2fee__lte=upper)
    else:
        target_kind = collection.filter(k2fee__gte=lower, k2fee__lte=upper)
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
    query.replace("home", zip_home)
    query.replace("school", zip_school)
    with urllib.request.urlopen(query) as url:
        data = json.loads(url.read().decode())
        dist = data['routes'][0]['legs'][0]['distance']['value']
        return dist

# def send(request):
#         p = Publisher(name='Apress', city='Berkeley')
#         p.save()
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