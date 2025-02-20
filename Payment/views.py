from django.shortcuts import render,HttpResponse
from .shipping_forms import ShipppingForm
from .models import ShippingAddress
# Create your views here.


def checkout(request):
    
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        shipping_form = ShipppingForm(request.POST or None, instance=shipping_user)


        return render(request,"checkout.html",{"shipping_form":shipping_form})
    
    else:
        shipping_form = ShipppingForm(request.POST or None)

        return render(request,"checkout.html",{"shipping_form":shipping_form})


        

def payment_success(request):

    return render(request,"payment.html")


