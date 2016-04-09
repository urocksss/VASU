from django.contrib.auth.models import User
from django.db import models

# Create your models here.

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


class FeeStruct(models.Model):
    course_type = models.CharField(max_length=5)
    branch = models.CharField(max_length=25)
    sem = models.IntegerField()
    fees = models.IntegerField()
    is_handi = models.BooleanField(default=False)
    category = models.CharField(max_length=3)
    year = models.IntegerField()


class Transactions(models.Model):
    stud_id = models.ForeignKey(StudentInfo)
    fee_id = models.ForeignKey(FeeStruct)
    pay_time = models.DateTimeField()
    trans_id = models.CharField(max_length=20)  # from bank after completion


class TempTrans(models.Model):
    stud_id = models.ForeignKey(StudentInfo)
    fee_id = models.ForeignKey(FeeStruct)
    pay_time = models.DateTimeField()
    unique_id=models.CharField(max_length=25)

class MapUserStud(models.Model):
    stud_id=models.OneToOneField(StudentInfo,related_name='stud_map')
    user=models.OneToOneField(User,related_name='user_map')