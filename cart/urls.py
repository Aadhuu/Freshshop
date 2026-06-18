"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cart import views

app_name='cart'
urlpatterns = [
    path('addtocart/<int:i>',views.AddtoCart.as_view(),name='addtocart'),
    path('cartview',views.CartView.as_view(),name='cartview'),
    path('cartremove/<int:i>',views.CartRemove.as_view(),name='cartremove'),
    path('cartdecrement/<int:i>',views.CartDecrement.as_view(),name='cartdecrement'),
    path('checkout',views.Checkout.as_view(),name='checkout'),
    path('success',views.PaymentSuccess.as_view(),name='success'),
    path('ordersummary',views.OrderSummary.as_view(),name='ordersummary'),

]
