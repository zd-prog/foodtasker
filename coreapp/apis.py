import json
from lib2to3.pgen2 import token
from os import access
from venv import create

from django.http import JsonResponse
from coreapp.models import OrderDetails, Restaurant, Meal, Order
from coreapp.serializers import OrderSerializer, RestaurantSerializer, \
MealSerializer, OrderStatusSerializer

from django.utils import timezone
from coreapp.views import restaurant_account
from oauth2_provider.models import AccessToken
from django.views.decorators.csrf import csrf_exempt

# ========
# RESTAURANT
# ========

def restaurant_order_notification(request, last_request_time):
  notification = Order.objects.filter(
    restaurant=request.user.restaurant, create_at__gt=last_request_time
    ).count()

  return JsonResponse({"notification": notification})

# ========
# CUSTOMER
# ========

def customer_get_restaurants(request):
  restaurants = RestaurantSerializer(
    Restaurant.objects.all().order_by("-id"),
    many=True,
    context={"request": request}
  ).data
  return JsonResponse({"restaurants": restaurants})

def customer_get_meals(request, restaurant_id):
  meals = MealSerializer(
    Meal.objects.filter(restaurant_id=restaurant_id).order_by("-id"),
    many=True,
    context={"request": request}
  ).data
  return JsonResponse({"meals":meals})

@csrf_exempt
def customer_add_order(request):
  """
    params:
      1. access_token
      2. restaurant_id
      3. address
      4. order_details (json format), example:
        [{"meal_id": 1, "quantity": 2}]
    return:
      {"status": "success"}
  """
  
  if request.method == "POST":
    # Get access token
    access_token = AccessToken.objects.get(token=request.POST.get("access_token"), expires__gt = timezone.now()
    )

    # Get customer profile
    customer = access_token.user.customer

    # Check whether customer has any outstanding order
    if Order.objects.filter(customer=customer).exclude(status=Order.DELIVERED):
      return JsonResponse({"status": "failed", "error": "Your last order must be completed"})

    # Check order's address
    if not request.POST["address"]:
      return JsonResponse({"status": "failed", "error": "Address is required"})

    # Get order details
    order_details = json.loads(request.POST["order_details"])

    # Check if meals in only one restaurant and then calculate the order total
    order_total = 0
    for meal in order_details:
      if not Meal.objects.filter(id=meal["meal_id"], restaurant_id=request.POST["restaurant_id"]):
        return JsonResponse({"status": "failed", "error": "Meal must be in only one restaurant"})
      else:
        order_total += Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]

    # CREATE ORDER   
    if len(order_details) > 0:
      # Step 1 - Create an Order
      order = Order.objects.create(
        customer = customer,
        restaurant_id = request.POST["restaurant_id"],
        total = order_total,
        status = Order.COOKING,
        address = request.POST["address"]
      )

      # Step 2 - Create Order Details 
      for meal in order_details:
        OrderDetails.objects.create(
          order = order,
          meal_id = meal["meal_id"],
          quantity = meal["quantity"],
          sub_total = Meal.objects.get(id=meal["id"]).price * meal["quantity"]
        )

      return JsonResponse({"status": "success"})

  return JsonResponse({})

def customer_get_latest_order(request):
  """
    params:
      1. access_token
    return:
      {JSON data with all details of an order}
  """

  access_token = AccessToken.objects.get(
    token = request.POST.get("access_token"),
    expires__gt = timezone.now()
  )
  customer = access_token.user.customer

  order = OrderSerializer(
    Order.objects.filter(customer=customer).last()
  ).data
  return JsonResponse({
    "last_order": order
  })

def customer_get_latest_order_status(request):
  """
    params:
      1. access_token
    return:
      {JSON data with all details of an order}
  """

  access_token = AccessToken.objects.get(
    token = request.POST.get("access_token"),
    expires__gt = timezone.now()
  )
  customer = access_token.user.customer

  order_status = OrderStatusSerializer(
    Order.objects.filter(customer=customer).last()
  ).data
  return JsonResponse({
    "last_order_status": order_status
  })

# ========
# DRIVER
# ========

def driver_get_ready_orders(request):
  return JsonResponse({})

def driver_get_pick_order(request):
  return JsonResponse({})

def driver_get_latest_order(request):
  return JsonResponse({})

def driver_complete_order(request):
  return JsonResponse({})

def driver_get_revenue(request):
  return JsonResponse({})