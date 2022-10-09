from dataclasses import field
from email.mime import image
from urllib import request
from rest_framework import serializers
from coreapp.models import Restaurant, Meal

class RestaurantSerializer(serializers.ModelSerializer):
  logo = serializers.SerializerMethodField()

  def get_logo(self, restaurant):
    request = self.context.get('request')
    logo_url = restaurant.logo.url
    return request.build_absolute_uri(logo_url)

  class Meta:
    model = Restaurant
    fields = ("id", "name", "phone", "address", "logo")

class MealSerializer(serializers.ModelSerializer):
  image = serializers.SerializerMethodField()

  def get_image(self, restaurant):
    request = self.context.get('request')
    image_url = restaurant.image.url
    return request.build_absolute_uri(image_url)

  class Meta:
    model = Meal
    fields = ("id", "name", "short_description", "image", "price")