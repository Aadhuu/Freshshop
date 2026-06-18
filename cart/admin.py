from django.contrib import admin

from cart.models import Cart

from cart.models import Order

from cart.models import OrderItem

admin.site.register(Cart)

admin.site.register(Order)
admin.site.register(OrderItem)

