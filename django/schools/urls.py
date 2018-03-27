from django.urls import path
from .views import SchoolListView, SchoolDetailView, saveToList, guild_search, advanced_search

urlpatterns = [
	path('guide_search/', guild_search, name='school'),
	path('advance/', advanced_search, name='detail'),
	path('', SchoolListView.as_view(), name='kindergarten-list'),
	path('<int:pk>/', SchoolDetailView.as_view(), name='school-detail'),
	path(r'^(?P<pk>)/$', saveToList, name='saveToList')
]
