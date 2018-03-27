from django.shortcuts import render
from django.http import HttpResponse
from .models import CompareList
from users.models import User
from schools.models import School

def index(request):
    result(request,'data')

def add(request,u,s):
    #cl=CompareList.objects.Create(user=u,school=s)
    if type(u)==User and type(s)==School and u and s: # not blank
        relation=CompareList(user=u,school=s)
        relation.save()
        return HttpResponse('add to compare list succeeded.')
    else:
        return HttpResponse('add to compare list failed.')

def remove(request,u,s):
    #cl=CompareList.objects.filter(user__name=uname,school__name=sname)
    cl=CompareList.objects.filter(user=u,school=s).delete()
    return HttpResponse("%s deleted from %s's compare list".format(s,u))

def result(request,u,order_by='data'):
    compareList=CompareList.objects.order_by(order_by).filter(user=u)
    #my_dict={'compareList':'This is from compare.'}
    return render(request,'compare.html',context=compareList)
