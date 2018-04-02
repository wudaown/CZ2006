from django.conf.urls import url
from django.urls import path
from compare import views

urlpatterns = [
    path('add/', views.add, name='compare_add'),
    path('remove/', views.remove, name='compare_remove'),
    path('remove_all/', views.remove_all, name='compare_remove_all'),
    path('<order_by>/', views.result, name='compare_result'),
    # passing in based on what to order by! default is by price
]
