from django.urls import path

from . import views

urlpatterns = [
    path('', views.guild_search, name='school'),
    # ex: /polls/5/
    path('advance/', views.advanced_search, name='detail'),
]