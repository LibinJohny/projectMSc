from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Login(AbstractUser):
    user_type=models.CharField(max_length=30)
    view_password=models.CharField(max_length=30)

class Department(models.Model):
    departmentname=models.CharField(max_length=30)

class DoctorReg(models.Model):
    doc_login=models.ForeignKey(Login,on_delete=models.CASCADE)
    doc_image=models.ImageField()
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.CharField(max_length=30)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    availabledays=models.CharField(max_length=10,null=True)
    timefrom=models.TimeField(null=True)
    timeto=models.TimeField(null=True)

class UserReg(models.Model):
    user_login=models.ForeignKey(Login,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.CharField(max_length=30)
    age=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    address=models.TextField()

class Appointment(models.Model):
    user=models.ForeignKey(UserReg,on_delete=models.CASCADE)
    doctor=models.ForeignKey(DoctorReg,on_delete=models.CASCADE)
    appointment_date=models.DateField()
    slottime=models.CharField(max_length=30,null=True)
    appointment_status=models.CharField(max_length=30,default='Booked')
    booked_date=models.DateField(auto_now=True,null=True)
    feedback_status=models.CharField(max_length=30,default='Empty')

class Feedback(models.Model):
    appointment=models.ForeignKey(Appointment,on_delete=models.CASCADE)
    feedback_text=models.TextField()