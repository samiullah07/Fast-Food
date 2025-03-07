from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm
from django.contrib import messages
import json
from cart.Cart import Cart
from Payment.models import ShippingAddress
from Payment.shipping_forms import ShipppingForm
# Create your views here.

# @login_required(login_url="/login/")
def HomePage(request):

    pro_objs = ProductDetail.objects.all()
    

    return render(request, "Index.html",{"pro_objs":pro_objs})

# @login_required(login_url="/login/")
def PizzaPage(request):
    pro_objs = ProductDetail.objects.filter(category__cat_name="Pizza")

    return render(request,"pizza.html",{"pro_objs":pro_objs})


# @login_required(login_url="/login/")
def BurgerPage(request):
    pro_objs = ProductDetail.objects.filter(category__cat_name="Burgers")

    return render(request,"burgers.html",{"pro_objs":pro_objs})



def LoginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Successful login
            login(request, user)

            # Handle saved cart if available
            current_user = Profile.objects.get(user=request.user)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product_id=key, quantity=value)
            
            messages.success(request, "You have logged in successfully!")
            return redirect('Home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
            return redirect('login')  # Stay on login page if authentication fails
    else:
        return render(request, 'login.html', {})



def LogoutPage(request):
    """
    Log the user out and redirect to home page with a success message.
    """
    logout(request)
    return redirect('Home')



def RegisterPage(request):
    """
    Handle user registration. If the form is valid, create a new user and log them in.
    """
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the form data to create a user
            user = form.save()

            # Authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Account created successfully. Welcome!")
                return redirect('user_info')  # Redirect to the home page after login
            else:
                messages.error(request, "Login failed. Please try again.")
                return redirect('login')  # Redirect back to login
        else:
            # Print form errors to debug why it's invalid
            print(form.errors)  # Debugging purposes
            messages.error(request, "Registration failed. Please try again.")
            return redirect('register')  # Redirect back to register
    else:
        return render(request, 'register.html', {'form': form})

def User_Profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)


        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,"User has been updated successfully")
            return redirect("Home")
        return render(request,"user_profile.html",{"user_form":user_form})
    else:
        messages.error(request,"You need to Login first")



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Password Changed")
                login(request,current_user)
                return redirect("Home")
            else:
                for error in list(form.errors.values()):
                    print(error)
                    return redirect("update_password")


        else:
            form = ChangePasswordForm(current_user)
            return render(request,"update_password.html",{"form":form})

    else:
        messages.error(request,"You need to login First")
        return redirect("Home")


def user_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id = request.user.id)

        form = UserInfoForm(request.POST or None,instance=current_user)

        
        #Shipping address form and user

        shipping_user= ShippingAddress.objects.get(user__id = request.user.id)
        shipping_form = ShipppingForm(request.POST or None, instance=shipping_user)


        if form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request,"User Info updated")
            return redirect("user_info")





        return render(request,"user_info.html",{"form":form,"shipping_form":shipping_form})
    
    else:
        return redirect("Home")


def getApi(request):
    payload = []

    orders = Order.objects.all()

    for order in orders:
        payload.append({
            "Product Details" : order.productDetail.product_name,
            "Price" : order.productDetail.prduct_price,
            "Username" : order.customer.first_name,
            "Address" : order.address,
            "quantity" : order.quanitiy,
            "date" : order.date,
            "status" : order.status,
        })



    return JsonResponse(payload,safe=False)


