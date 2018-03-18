from django.urls import path
from .views import LoginView, RegisterView, ForgetPasswordView

urlpatterns = [
	path('', LoginView.as_view(), name='login'),
	path('login/', LoginView.as_view(), name='login'),
	path('register/', RegisterView.as_view(), name='register'),
	path('forget/', ForgetPasswordView.as_view(), name='forget')
]