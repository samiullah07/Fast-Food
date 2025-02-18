from django.shortcuts import render,HttpResponse

# Create your views here.


def payment_success(request):

    return render(request,"payment.html")