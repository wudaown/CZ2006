from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import School, Kindergarten
from django.utils import timezone
from users.models import User

# Create your views here.

# todo: a detailView and a ListView with paging
def school_info(request, centre_code):
    school = School.object.all()

    return HttpResponse("You are look at school %s.".format(name))


class SchoolListView(ListView):
    model = Kindergarten

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class SchoolDetailView(DetailView):

    model = Kindergarten
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def saveToList(request,pk):
    try:
        user = User.objects.get(username=request.session['member_id'])
    except:
        #print('here')
        return render(request, 'login.html')
    school = Kindergarten.objects.get(id = pk)
    user.following.add(school)
    user.save()
    #print('ok')
    return HttpResponse("<script>Save.Response_OK();</script>")
