from django.core.mail import send_mail
from schools.models import School
from djangoTut.settings import EMAIL_HOST_USER
import random
import string

from users.models import EmailVerifyRecord


def active_generator(n):
	return ''.join(random.choice(string.ascii_uppercase + string.digits, k=n))


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
	baseurl = 'https://www.msf.gov.sg/dfcs/kindergarten/view.aspx?id='
	num = 1
	url = baseurl + str(num)

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
		
	