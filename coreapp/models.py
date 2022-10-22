from email.policy import default
import imp
from lib2to3.pgen2 import driver
from random import choices
from time import time
from django.db.models.deletion import CASCADE
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone

# Create your models here.
class Restaurant(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
  name = models.CharField(max_length=255)
  phone = models.CharField(max_length=255)
  address = models.CharField(max_length=255)
  logo = CloudinaryField('image')

  def __str__(self):
    return self.names

class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
  avatar = models.CharField(max_length=255)
  phone = models.CharField(max_length=255, blank=True)
  address = models.CharField(max_length=255, blank=True)

  def __str__(self):
    return self.user.get_full_name()

class Driver(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
  avatar = models.CharField(max_length=255)
  car_model = models.CharField(max_length=255, blank=True)
  plate_number = models.CharField(max_length=255, blank=True)
  location = models.CharField(max_length=255, blank=True)

  def __str__(self):
    return self.user.get_full_name()

class Meal(models.Model):
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant')
  name = models.CharField(max_length=255)
  short_description = models.TextField(max_length=500)
  image = CloudinaryField('image')
  price = models.IntegerField(default=0)

  def __str__(self):
    return self.name

class Order(models.Model):
  COOKING = 1
  READY = 2
  ONTHEWAY = 3
  DELIVERED = 4

  STATUS_CHOISES = (
    (COOKING, "Cooking"),
    (READY, "Ready"),
    (ONTHEWAY, "On the way"),
    (DELIVERED, "Delivered"),
  )

  customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
  driver = models.ForeignKey(Driver, models.SET_NULL, blank=True, null=True)
  address = models.CharField(max_length=500)
  total = models.IntegerField()
  status = models.IntegerField(choices=STATUS_CHOISES)
  created_at = models.DateTimeField(default=timezone.now)
  picked_at = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return str(self.id)

class OrderDetails(models.Model):
  order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_details')
  meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
  quantity = models.IntegerField()
  sub_total = models.IntegerField()

  def __str__(self):
    return str(self.id)