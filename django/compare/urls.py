from django.conf.urls import url
from django.conf.urls import include
from compare import views

urlpatterns = [
    url(r'^$',views.add,name='add'),
    url(r'^$',views.remove,name='remove'),
    url(r'^$',views.result,name='result'),
    #url(r'^$',views.index,name='index'),
]
