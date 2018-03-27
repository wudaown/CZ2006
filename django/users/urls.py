from django.urls import path
from .views import LoginView, RegisterView, ForgetPasswordView, LogoutView,UserPageView

urlpatterns = [
	# path('', LoginView.as_view(), name='login'),
	# path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('register/', RegisterView.as_view(), name='register'),
	path('forget/', ForgetPasswordView.as_view(), name='forget'),
	path('<slug:username>/', UserPageView.as_view(),name='user_page'),
]