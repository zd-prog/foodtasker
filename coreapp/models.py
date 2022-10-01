from email.policy import default
import imp
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

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