from doctest import FAIL_FAST
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from coreapp.forms import AccountForm, UserForm, RestaurantForm, MealForm
from coreapp.models import Meal, Order

# Create your views here.
def home(request):
  return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign_in/')
def restaurant_home(request):
  return redirect(restaurant_order)

def restaurant_sign_up(request):
  user_form = UserForm()
  restaurant_form = RestaurantForm()

  if request.method == "POST":
    user_form = UserForm(request.POST)
    restaurant_form = RestaurantForm(request.POST, request.FILES)

    if user_form.is_valid() and restaurant_form.is_valid():
      new_user = User.objects.create_user(**user_form.cleaned_data)
      new_restaurant = restaurant_form.save(commit=False)
      new_restaurant.user = new_user
      new_restaurant.save()

      login(request, authenticate(
        username = user_form.cleaned_data["username"], password = user_form.cleaned_data["password"],
      ))

      return redirect(restaurant_home)

  return render(request, "restaurant/sign_up.html", {
    "user_form": user_form,
    "restaurant_form": restaurant_form
  })
  
@login_required(login_url='/restaurant/sign_in/')
def restaurant_account(request):

  if request.method == "POST":
    account_form = AccountForm(request.POST, instance=request.user)
    restaurant_form = RestaurantForm(request.POST, request.FILES, instance=request.user.restaurant)

    if account_form.is_valid() and restaurant_form.is_valid():
      account_form.save()
      restaurant_form.save()
    
  account_form = AccountForm(instance=request.user)
  restaurant_form = RestaurantForm(instance=request.user.restaurant)

  return render(request, 'restaurant/account.html', {
    "account_form": account_form,
    "restaurant_form": restaurant_form
  })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_meal(request):
  meals = Meal.objects.filter(restaurant=request.user.restaurant).order_by("-id")
  return render(request, 'restaurant/meal.html', {
    "meals": meals
  })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_add_meal(request):

  if request.method == "POST":
    meal_form = MealForm(request.POST, request.FILES)

    if meal_form.is_valid():
      meal = meal_form.save(commit=False)
      meal.restaurant = request.user.restaurant
      meal.save()
      return redirect(restaurant_meal)


  meal_form = MealForm()
  return render(request, 'restaurant/add_meal.html', {
    "meal_form": meal_form
  })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_edit_meal(request, meal_id):

  if request.method == "POST":
    meal_form = MealForm(request.POST, request.FILES, instance=Meal.objects.get(id=meal_id))

    if meal_form.is_valid():
      meal_form.save()
      return redirect(restaurant_meal)

  meal_form = MealForm(instance=Meal.objects.get(id=meal_id))
  return render(request, 'restaurant/edit_meal.html', {
    "meal_form": meal_form
  })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_order(request):
  if request.method == "POST":
    order = Order.objects.get(id=request.POST["id"])

    if order.status == Order.COOKING:
      order.status = Order.READY
      order.save()
      
  orders = Order.objects.filter(restaurant = request.user.restaurant).order_by("-id")
  return render(request, 'restaurant/order.html', {
    "orders": orders
  })

@login_required(login_url='/restaurant/sign_in/')
def restaurant_report(request):
  return render(request, 'restaurant/report.html', {})