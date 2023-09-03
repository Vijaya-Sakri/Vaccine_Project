from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Vaccine(models.Model):
    vid = models.AutoField(primary_key=True)
    user= models.ForeignKey(User,on_delete=models.CASCADE,default="Free")
    vname = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=500)
    sideEffects = models.CharField(max_length=500)
    ingredients = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    
class User_Vaccines(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,default="Free")
    vid = models.ForeignKey(Vaccine,on_delete=models.CASCADE,default="Free")

class profile_image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True)

class appointment(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,default="Free")
    child_name = models.CharField(max_length = 100)
    child_age = models.IntegerField()
    centre = models.CharField(max_length=200)
    date = models.DateField()

class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    message = models.CharField(max_length=500)