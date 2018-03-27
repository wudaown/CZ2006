from django.conf.urls import url
from compare import views

urlpatterns = [
    url(r'^$',views.add,name='add'),
    url(r'^$',views.remove,name='remove'),
    url(r'^$',views.result,name='result'),
]
