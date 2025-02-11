from django.urls import path
from .views import *
urlpatterns = [
    path("",cart_summary,name="cart"),
    path("add/",cart_add,name="cart_add"),
    path("update_cart/",update_cart,name="update")

]
