from django.contrib import admin

from .models import (
    Country,
    CreditCard,
    Dish,
    DishType,
    LastVisitedRestaurants,
    Order,
    Photo,
    Restaurant,
    User,
)

admin.site.register(User)
admin.site.register(Photo)
admin.site.register(DishType)
admin.site.register(Dish)
admin.site.register(Country)
admin.site.register(LastVisitedRestaurants)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(CreditCard)
