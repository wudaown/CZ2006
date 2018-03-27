from django import forms


class LoginForm(forms.Form):
	uname = forms.CharField(required=True)
	# https://docs.djangoproject.com/en/2.0/ref/forms/fields/#built-in-field-classes
	# https://stackoverflow.com/questions/9324432/how-to-create-password-input-field-in-django
	passwd = forms.CharField(widget=forms.PasswordInput, required=True, min_length=6, error_messages={'min_length': 'undefined'})
	
	
class RegisterForm(forms.Form):
	#todo: username validation,cannot start with numbers
	username = forms.CharField(required=True, min_length=6)
	password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=6)
	email = forms.EmailField(required=True)
	

