"""djangoTut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index
from users.views import ActiveView, ResetView
# from schools.admin import admin_site
import xadmin
from django.views.generic import TemplateView

urlpatterns = [
	# path('', TemplateView.as_view(template_name='index.html'), name='index'),
	path('', index, name='index'),
	#path('xadmin/', xadmin.site.urls),
	path('admin/', admin.site.urls),
	path('schools/',include('schools.urls'),name = 'schools'),
	path('users/', include('users.urls'), name='users'),
	path('schools/', include('schools.urls'), name='schools'),
	path('active/<slug:active_code>/', ActiveView.as_view(), name='active'),
	path('reset/<slug:reset_code>/', ResetView.as_view(), name='reset')
	# path('login/', TemplateView.as_view(template_name='login.html'), name='login')
	# path('myadmin/', admin_site.urls)
]
