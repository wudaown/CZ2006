from django.conf.urls import url
from django.urls import path
from compare import views

urlpatterns = [
<<<<<<< HEAD
    #path('add/', views.add, name='compare_add'),
    #path('remove/', views.remove, name='compare_remove'),
    #path('<order_by>/', views.result, name='compare_result'),
    # passing in based on what to order by!
=======
    path('add/', views.add, name='compare_add'),
    path('remove/', views.remove, name='compare_remove'),
    path('remove_all/', views.remove_all, name='compare_remove_all'),
    path('<order_by>/', views.result, name='compare_result'),
    # passing in based on what to order by! default is by price
>>>>>>> 65ca491ff9100df14858c2c02c35ce99efccc3e5
]
