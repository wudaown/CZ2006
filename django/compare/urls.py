from django.conf.urls import url
from django.conf.urls import include
from compare import views #AH

urlpatterns = [
	# path('', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$',views.add,name='add'),
    url(r'^$',views.remove,name='remove'),
    url(r'^$',views.result,name='result'),
    url(r'^$',views.index,name='index'),
]
