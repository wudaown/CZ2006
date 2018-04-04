from django.urls import path
from .views import SchoolDetailView, advanced_search, ToggleFav, GuideSearch

urlpatterns = [
	path('search_by_details/', GuideSearch.as_view(), name='detail'),
	path('advance/', advanced_search, name='advance'),
	path('<int:pk>/', SchoolDetailView.as_view(), name='kindergarten-detail'),
	path('save/<int:pk>', ToggleFav.as_view(), name='toggle-fav'),
]
