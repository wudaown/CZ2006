from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from .models import School, Kindergarten
from django.utils import timezone
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

        k2=False
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
    query = query.replace("home", str(zip_home))
    query = query.replace("school", str(zip_school))
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

    
# class SchoolListView(ListView):
#     model = Kindergarten
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context

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
        
        return render(request, 'schoolList.html', {'kindergarten': kindergarten})

class SchoolDetailView(DetailView):

    model = Kindergarten
    def school_detail_view(self,request,pk):
        try:
            school_id = Kindergarten.objects.get(pk=pk)
        except Kindergarten.DoesNotExist:
            raise Http404("Kindergarten does not exist")

            # book_id=get_object_or_404(Book, pk=pk)
        if User.objects.get(username=request.session['member_id']) is not None:
            user = User.objects.get(username=request.session['member_id'])

            return render(
                request,
                'school-detail',
                context={'kindergarten': school_id, 'user ':user,}
            )
        else:
            return render(
                request,
                'school-detail',
                context={'kindergarten': school_id, 'user ': None, }
            )

'''    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
        '''

def saveToList(request,pk):
    try:
        user = User.objects.get(username=request.session['member_id'])
    except:
        #print('here')
        return render(request, 'login.html')
    school = Kindergarten.objects.get(id = pk)
    if school in user.following.all():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        user.following.add(school)
        user.save()
    #print('ok')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def deleteFromList(request,pk):
    try:
        user = User.objects.get(username=request.session['member_id'])
    except:
        #print('here')
        return render(request, 'login.html')
    school = Kindergarten.objects.get(id = pk)
    if school in user.following.all():
        user.following.remove(school)
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
