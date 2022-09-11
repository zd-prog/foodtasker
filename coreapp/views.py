from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
  return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign_in/')
def restaurant_home(request):
  return render(request, "restaurant/home.html", {})

def restaurant_sign_up(request):
  return render(request, "restaurant/sign_up.html", {})