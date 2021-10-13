from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models.deletion import CASCADE


# Create your models here.
class Products(models.Model):
    Item=models.CharField(max_length=100)
    Featured=models.BooleanField()
    ImgCDN=models.CharField(max_length=500,null=True,blank=True)
    Price=models.FloatField()
    Description=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.Item


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    ItemID=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='Itemid')
    Quantity=models.IntegerField(default=0)

class Address(models.Model):
    Name=models.ForeignKey(User,on_delete=CASCADE)
    Phone=models.CharField(max_length=15)
    address=models.TextField()
   

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    Phone=models.CharField(max_length=10)
    Address=models.TextField()
    Items=models.TextField(null=True,blank=True)
    Total=models.FloatField()
    
