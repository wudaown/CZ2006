from django.core.mail import send_mail
from schools.models import School, Kindergarten, Language
from djangoTut.settings import EMAIL_HOST_USER
from requests_html import HTMLSession
import random
import string

from users.models import EmailVerifyRecord


def active_generator(n):
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def send_verify_mail(email, mail_type=0):
	random_code = active_generator(10)
	vemail = EmailVerifyRecord()
	vemail.email = email
	vemail.code = random_code
	vemail.code_type = 0
	vemail.save()
	
	if mail_type == 0:
		email_subject = 'Activation Link'
		email_message = 'http://127.0.0.1:8000/active/{0}'.format(random_code)
	elif mail_type == 1:
		email_subject = "New Password"
		email_message = "http://127.0.0.1:8000/reset/{0}".format(random_code)
		
	send_status = send_mail(email_subject, email_message, EMAIL_HOST_USER, [email])
	
	if send_status:
		pass


def load_schools(filePath):
	file = open(filePath, 'r')
	a = []
	for i in file:
		a.append(i.strip('\n'))
	b = []
	for i in a:
		b.append(i.split(','))
	b.pop(0)
	for i in b:
		# r = School.objects.filter(centre_code=i[0])
		# if not r:
		sch = School()
		sch.centre_code = i[0]
		sch.centre_name = i[1]
		sch.level = i[2]
		sch.program_hours = i[3]
		sch.language = i[4]
		if i[5] == 'na':
			sch.vacancy = False
		else:
			sch.vacancy = True
		try:
			sch.registration_fee = float(i[6])
			sch.fee = float(i[7])
		except Exception as e:
			sch.registration_fee = float(0)
			sch.fee = float(0)
		sch.save()
	else:
		pass
	
	
def crawler():
	session = HTMLSession()
	baseurl = 'https://www.msf.gov.sg/dfcs/kindergarten/view.aspx?id='
	lang = Language.objects.all()
	# chinese = lang[0]
	# tamil = lang[1]
	# hindi = lang[2]
	# malay = lang[3]
	# arabic = lang[4]
	for i in range(1, 449):
		print(i)
		url = baseurl + str(i)
		r = session.get(url)
		a = r.html.find('table', first=True).find('td')[:-1]
		kinder = Kindergarten()
		# for i in a[1::2]:
		a = a[1::2]
		kinder.name = a[0].text
		if a[1].text == 'Active':
			kinder.isoperation = True
		else:
			kinder.isoperation = False
		kinder.type = a[2].text
		kinder.address = a[3].text
		kinder.postalcode = a[4].text
		kinder.email = a[5].text
		try:
			kinder.number = int(a[6].text)
		except ValueError:
			kinder.number = a[6].text[:8]
		kinder.website = a[7].text
		kinder.facebook = a[8].text
		if a[9].text.isnumeric():
			kinder.capacity = a[9].text
		# try:
		# except ValueError:
		else:
			kinder.capacity = int(a[9].text.split(';')[0])
		if a[10].text == 'Yes':
			kinder.outdoor = True
		else:
			kinder.outdoor = False
		if a[11].text == 'Yes':
			kinder.bus = True
		else:
			kinder.bus = False
		if a[12].text == 'Yes':
			kinder.sparkCer = True
			kinder.sparkvalidity = a[13].text
		else:
			kinder.sparkCer = False
			kinder.sparkvalidity = 'NULL'
		a = r.html.find('table.tb_fees')[0].find('td')[1::3]
		kinder.registrationfee = a[0].text
		kinder.k2fee = a[1].text
		kinder.k1fee = a[2].text
		kinder.nurseryfee = a[3].text
		kinder.prenurseryfee = a[4].text
		kinder.playgroupfee = a[5].text
		a = r.html.find('tr', containing='Second')[0].find('td')[1]
		b = a.text.split('\n')
		for i in b:
			if i != 'No':
				for l in lang:
					if i == l.language:
						kinder.save()
						kinder.language.add(l)
		# a = r.html.find('tr', containing='Other Language')[0].find('td')[1]
		# b = a.text.split('\n')
		# for i in b:
		# 	language = language()
		# 	if i != 'No':
		# 		language.language = i
		# 		language.save()
		
	kinder.save()

            

# def load_level(filePath):
# 	file = open(filePath, 'r')
# 	# r = Level.objects.all()
# 	# pg = r[0]
# 	# pre = r[1]
# 	# k1 = r[2]
# 	# k2 = r[3]
# 	# nur = r[4]
# 	a = []
# 	for i in file:
# 		a.append(i.strip('\n'))
# 	b = []
# 	for i in a:
# 		b.append(i.split(','))
# 	b.pop(0)
# 	for i in b:
# 		sch = School.objects.filter(centre_code=i[0])[0]
# 		level = Level()
# 		if i[5] == 'na':
# 			level.vacancy = False
# 		else:
# 			level.vacancy = True
# 		if i[2] == 'Playgroup':
# 			level.level = 'Playgroup'
# 			level.save()
# 			level.kindergarten.add(sch)
# 		elif i[2] == 'Pre-Nursery':
# 			level.level = 'Pre-Nursery'
# 			level.save()
# 			level.kindergarten.add(sch)
# 		elif i[2] == 'Kindergarten 1':
# 			level.level = 'Kindergarten 1'
# 			level.save()
# 			level.kindergarten.add(sch)
# 		elif i[2] == 'Kindergarten 2':
# 			level.level == 'Kindergarten 2'
# 			level.save()
# 			level.kindergarten.add(sch)
# 		elif i[2] == 'Nursery':
# 			level.level = 'Nursery'
# 			level.save()
# 			level.kindergarten.add(sch)
# 		level.save()
#
		
	
