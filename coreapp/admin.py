from django.contrib import admin
from coreapp.models import Restaurant, Customer, Driver, Meal
# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Meal)