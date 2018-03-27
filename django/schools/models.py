# _*_ encoding:utf-8 _*_

from django.db import models
from datetime import datetime
# Create your models here.




class Language(models.Model):
	language = models.CharField(choices=(('Chinese', 'Chinese'), ('Tamil', 'Tamil'), ('Hindi', 'Hindi'), ('Malay', 'Malay'), ('Arabic', 'Arabic')), max_length=20, verbose_name='Language')

	class Meta:
		verbose_name = 'Language'
		verbose_name_plural = 'Languages'

	def __str__(self):
		return self.language


class Kindergarten(models.Model):
	name = models.CharField(max_length=100, null=False, verbose_name="Centre Name")
	isoperation = models.BooleanField(default=True, verbose_name="Operation Status")
	type = models.CharField(max_length=50, verbose_name="Kindergarten Type")
	address = models.CharField(max_length=100, null=False, verbose_name='Centre Address')
	postalcode = models.IntegerField(verbose_name='Postal Code')
	email = models.EmailField(verbose_name='Centre Email Address')
	website = models.URLField(max_length=100, verbose_name='Website')
	number = models.IntegerField(verbose_name='Centre Contact Number')
	facebook = models.CharField(max_length=100, verbose_name="Facebook")
	k1_capacity = models.IntegerField(default=0, verbose_name="Accomodation Capacity")
	k2_capacity = models.IntegerField(default=0, verbose_name="Accomodation Capacity")
	outdoor = models.BooleanField(verbose_name="Provision of outdoor playground/garden")
	bus = models.BooleanField(verbose_name='Bus Service')
	sparkCer = models.BooleanField(verbose_name='SPARK Certified')
	sparkvalidity = models.CharField(max_length=100, verbose_name="SPARK Validity (end)")
	registrationfee = models.CharField(max_length=10, verbose_name='Registration Fees')
	k2fee = models.CharField(max_length=10, verbose_name='Kindergarten Two Fees')
	k1fee = models.CharField(max_length=10, verbose_name='Kindergarten One Fees')
	nurseryfee = models.CharField(max_length=10, verbose_name='Nursery Fees')
	prenurseryfee = models.CharField(max_length=10, verbose_name='Pre-Nursery Fees')
	playgroupfee = models.CharField(max_length=10, verbose_name='Playgroup Fees')
	language = models.ManyToManyField(Language, verbose_name='Language Offered')
	#linkedUsers = models.ManyToManyField(User)
	
	class Meta:
		verbose_name = 'Kindergarten'
		verbose_name_plural = 'Kindergarten'
	
	def __str__(self):
		return self.name


class School(models.Model):
	centre_name = models.CharField(max_length=100, null=False, verbose_name='Centre Name')
	centre_code = models.CharField(max_length=20, null=False, verbose_name='Centre Code')
	program_hours = models.CharField(max_length=100, verbose_name='Program Hour')
	vacancy = models.BooleanField(default=False, verbose_name='Vacancy Available')
	registration_fee = models.FloatField(verbose_name='Registration Fee')
	fee = models.FloatField(verbose_name='Fees')
	level = models.CharField(default='', choices=(('Playgroup', 'Playgroup'), ('Pre-Nursery', 'Pre-Nursery'), ('Kindergarten 1', 'Kindergarten 1'), ('Kindergarten 2', 'Kindergarten 2'), ('Nursery', 'Nursery')),  max_length=20, verbose_name='Level')
	language = models.CharField(default='', choices=(('Chinese', 'Chinese'), ('Tamil', 'Tamil'), ('Hindi', 'Hindi'), ('Malay', 'Malay'), ('Arabic', 'Arabic')), max_length=20, verbose_name='Language')
	# TODO
	# This many to many relationship still having problem
	# level_offer = models.ManyToManyField(Level, verbose_name='Level Offer')
	# language_offer = models.ManyToManyField(Language, verbose_name='Language Offered')

	class Meta:
		verbose_name = 'Kindergarten'
		verbose_name_plural = 'Kindergartens'

	# def __unicode__(self):
	# 	return self.centre_code

	# Text to be display in the admin page
	# and other time where string need to
	# be display
	def __str__(self):
		return '{0} {1}'.format(self.centre_name, self.centre_code)



# class Level(models.Model):
# 	kindergarten = models.ManyToManyField(School, verbose_name='Kindergarten')
# 	level = models.CharField(choices=(('Playgroup', 'Playgroup'), ('Pre-Nursery', 'Pre-Nursery'), ('Kindergarten 1', 'Kindergarten 1'), ('Kindergarten 2', 'Kindergarten 2'), ('Nursery', 'Nursery')),  max_length=20, verbose_name='Level')
# 	vacancy = models.BooleanField(default=False, verbose_name='Vacancy Available')
#
# 	class Meta:
# 		verbose_name_plural = 'Levels'
# 		verbose_name = 'Level'
#
# 	def __str__(self):
# 		return self.level
