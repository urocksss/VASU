from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.http import request


class StudentInfo(models.Model):
    stud_id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    date_of_joining = models.DateField()
    course_type = models.CharField(max_length=5)
    branch = models.CharField(max_length=25)
    date_of_birth = models.DateField()
    category = models.CharField(max_length=3)
    gender = models.CharField(max_length=1)
    is_handi = models.BooleanField(default=False)
    def __unicode__(self):
       		return self.pk

class FeeStruct(models.Model):
    fee_type=models.CharField(max_length=10,default='Null')
    course_type = models.CharField(max_length=5)
    branch = models.CharField(max_length=25)
    sem = models.IntegerField()
    fees = models.IntegerField()
    is_handi = models.BooleanField(default=False)
    category = models.CharField(max_length=3)
    year = models.IntegerField()
    def __unicode__(self):
       		return self.fee_type


class Transactions(models.Model):
    stud_id = models.ForeignKey(StudentInfo)
    fee_id = models.ForeignKey(FeeStruct)
    pay_time = models.DateTimeField()
    trans_id = models.CharField(max_length=20)  # from bank after completion
    def __unicode__(self):
       		return self.trans_id


class TempTrans(models.Model):
    stud_id = models.ForeignKey(StudentInfo)
    fee_id = models.ForeignKey(FeeStruct)
    pay_time = models.DateTimeField()
    unique_id=models.CharField(max_length=25)
    def __unicode__(self):
       		return self.stud_id




