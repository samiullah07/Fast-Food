
from django.urls import path
from .views import *


urlpatterns = [
    path("payment/",payment_success,name="payment")
   
    ]

