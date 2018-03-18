# _*_ encoding:utf-8 _*_

from django.db import models
from datetime import datetime
import datetime as dt
from django.contrib.auth.models import AbstractUser

from schools.models import School

# Create your models here.


class User(AbstractUser):
	username = models.CharField(max_length=20, verbose_name='Username', unique=True)
	email = models.EmailField(max_length=40, verbose_name='Email')
	first_name = models.CharField(max_length=20, verbose_name='First Name')
	last_name = models.CharField(max_length=20, verbose_name='Last Name')
	date_join = models.DateTimeField(default=datetime.now)
	is_active = models.BooleanField(default=False)
	mobile = models.CharField(max_length=8, null=True, blank=True)
	following = models.ManyToManyField(School)

	class Meta:
		verbose_name = 'Users'
		verbose_name_plural = 'Users'

	def __unicode__(self):
		return self.username

	def __str__(self):
		return self.username


class EmailVerifyRecord(models.Model):
	register = 0
	forget_password = 1
	code = models.CharField(max_length=6, verbose_name='Verity Code')
	email = models.EmailField(max_length=40, verbose_name='Email')
	code_type = models.CharField(choices=((register, 'Register'), (forget_password, 'Forget Password')), max_length=20)
	# code_type = models.CharField(max_length=10, verbose_name="Code Type")
	send_time = models.DateTimeField(default=datetime.now, verbose_name='Send Time')
	# TODO
	# Expired time of the activation code
	# expired = models.DateTimeField(dt.date.today() + dt.timedelta(days=2))

	class Meta:
		verbose_name = 'Verify Email Address'
		verbose_name_plural = verbose_name
