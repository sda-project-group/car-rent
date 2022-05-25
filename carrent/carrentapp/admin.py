from django.contrib import admin
from django.contrib.auth.models import Group

from carrentapp.models import Car, CarModel, CarBrand, BasePrice, Order

admin.site.unregister(Group)
admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(CarBrand)
admin.site.register(BasePrice)
admin.site.register(Order)
