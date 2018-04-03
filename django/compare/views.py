from django.shortcuts import render
from django.http import HttpResponse
from users.models import CompareList
from users.models import User
from schools.models import Kindergarten

MAX_LIST_SIZE=3

def add(request, id):
    try:
        u = User.objects.get(username=request.session['member_id'])
    except:
        return render(request, 'login.html')

    if len(CompareList.objects.filter(user=u)) >= MAX_LIST_SIZE:
        return render(request, 'compare_modify.html', {'msg':
                                                       'Cannot add to compare because there are already 3 schools in compare.'})

    try:
        s = Kindergarten.objects.get(id=id)  # TODO
        relation = CompareList(user=u, school=s)
        if CompareList.objects.filter(user=u, school=s).exists():
            return render(request, 'compare_modify.html', {'msg': 'Add to compare list failed, already added!'})
        relation.save()
    except:
        return render(request, 'compare_modify.html', {'msg': 'Add to compare list failed.'})
    return render(request, 'compare_modify.html', {'msg': 'Add to compare list succeeded.'})

def remove(request, id):
    try:
        u = User.objects.get(username=request.session['member_id'])
    except:
        return render(request, 'login.html')

    s = Kindergarten.objects.get(id=id)  # TODO
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
