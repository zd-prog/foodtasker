from django.http import JsonResponse
from coreapp.models import Restaurant
from coreapp.serializers import RestaurantSerializer

def customer_get_restaurants(request):
  restaurants = RestaurantSerializer(
    Restaurant.objects.all().order_by("-id"),
    many=True
  ).data
  return JsonResponse({"restaurants": restaurants})