# _*_ encoding:utf-8 _*_

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from .models import User, EmailVerifyRecord
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password
from djangoTut.utils import send_verify_mail
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


class ActiveView(View):
	def get(self, request, active_code):
		record = EmailVerifyRecord.objects.filter(code=active_code)[0]
		user = User.objects.filter(email=record.email)[0]
		user.is_active = True
		user.save()
		# TODO
		# Invalid active code
		record.delete()
		return render(request, 'index.html')


class ResetView(View):
	# TODO
	# some more logic
	# felt something wrong
	# form validation
	def get(self, request, reset_code):
		record = EmailVerifyRecord.objects.filter(code=reset_code)
		if record:
			return render(request, 'reset.html')
		else:
			return HttpResponse('Invalid link')
	
	def post(self, request, reset_code):
		record = EmailVerifyRecord.objects.filter(code=reset_code)[0]
		user = User.objects.filter(email=record.email)[0]
		password = request.POST['password']
		cpassword = request.POST['cpassword']
		if password == cpassword:
			user.password = make_password(password)
			user.save()
			record.delete()
			return render(request, 'index.html')
		else:
			return render(request, 'reset.html', {'msg': 'Password does not match'})
			
			
class LoginView(View):
	def get(self, request):
		return render(request, 'login.html')
	
	def post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			username = request.POST['uname']
			passwd = request.POST['passwd']
			# passwd = request.POST.get('passwd')
			
			# username and password need to be specify
			user = authenticate(username=username, password=passwd)
			if user is not None:
				login(request, user)
				# return HttpResponseRedirect('login.html')
				return render(request, 'index.html')
			else:
				msg = {'msg': 'Username or Password Wrong'}
				return render(request, 'login.html', msg)
		else:
			error = login_form.errors
			errors = {'name_of_error': error}
			# To pass the parameter into html
			# the key inside the dict is use
			return render(request, 'login.html', errors)
	
	
class RegisterView(View):
	def get(self, request):
		register_form = RegisterForm()
		return render(request, 'register.html', {'register_form': register_form})
	
	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			username = register_form.data['username']
			password = register_form.data['password']
			email = register_form.data['email']
			if User.objects.filter(username=username):
				return render(request, 'register.html', {'msg': 'Username already exists'})
			user = User()
			# Only if email activation is needed then set is_active false
			user.is_active = False
			user.username = username
			user.email = email
			user.password = make_password(password)
			user.save()
			send_verify_mail(email)
			return render(request, 'index.html')
		else:
			# Actual not need
			# by using the django form in html
			# all validation is done hence
			# should not end up here
			error = register_form.errors
			errors = {'name_of_error': error}
			return render(request, 'register.html', errors)


class LogoutView(View):
	def get(self, request):
		logout(request)
		return render(request, 'index.html')


class ForgetPasswordView(View):
	# TODO
	# form validation
	def get(self, request):
		return render(request, 'forget.html')
	
	def post(self, request):
		email = request.POST['email']
		send_verify_mail(email, 1)
		return render(request, 'forget.html', {'msg': 'Submission done. Please your email'})
