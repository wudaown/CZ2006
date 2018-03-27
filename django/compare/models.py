from django.db import models
from users.models import User
from schools.models import School

class CompareList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    school = models.ForeignKey('School', on_delete=models.CASCADE)

    #rank_type = models.IntegerField()

    # def __str__(self):
    #     return self.name

# class CompareRecord(models.Model):
#     list=models.ForeignKey('CompareList',on_delete=models.CASCADE)
#     user = models.ManyToOneField(
#         User,
#         on_delete=models.CASCADE,
#         primary_key=True,)
#     school = user = models.ManyToOneField(
#         School,
#         on_delete=models.CASCADE,
#         primary_key=True,)
#     #compared = models.ForeignKey()#TODO
#
#     def __str__(self):
#         return self.name
