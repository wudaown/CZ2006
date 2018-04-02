# _*_ encoding:utf-8 _*_

from django.db import models
from datetime import datetime
import datetime as dt
from django.contrib.auth.models import AbstractUser
from schools.models import Kindergarten
#from compare.models import CompareList

# Create your models here.

#class DreamList(models.Model):
 #   username = models.ForeignKey('User',on_delete=models.CASCADE)
 #   schoolName = models.ForeignKey('Kindergarten',on_delete=models.CASCADE)


class Message_Mailbox(models.Model):
    mailbox = models.ForeignKey('MailBox', on_delete=models.CASCADE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)


class Message(models.Model):
    #from_id = models.OneToOneField('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)

class MailBox(models.Model):
    messages = models.ManyToManyField('Message', through=Message_Mailbox)

class CompareList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    school = models.ForeignKey('schools.Kindergarten', on_delete=models.CASCADE)

class User(AbstractUser):
    username = models.CharField(max_length=20, verbose_name='Username', unique=True)
    email = models.EmailField(max_length=40, verbose_name='Email')
    first_name = models.CharField(max_length=20, verbose_name='First Name')
    last_name = models.CharField(max_length=20, verbose_name='Last Name')
    date_join = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=False)
    mobile = models.CharField(max_length=8, null=True, blank=True)
    mailbox = models.OneToOneField(MailBox,on_delete=models.CASCADE,null=True)
    following = models.ManyToManyField(Kindergarten, related_name='following_kd')
    compare_schools=models.ManyToManyField(Kindergarten, related_name='compare_kd',through='CompareList')

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
