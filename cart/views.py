from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .Cart import Cart
from Products.models import ProductDetail
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import logging


def cart_summary(request):
    cart = Cart(request)

    products = cart.get_prods()
    total_items = len(products)
   

    total_price = sum(product.prduct_price for product in products)
    quantities = cart.get_quantities()
    print(quantities)
    
    context = {
        "products":products,
        "quantities" :quantities,
        "total_price" : total_price
        
	}


    return render(request, "cart.html",{"context":context})



logger = logging.getLogger(__name__)

def cart_add(request):
    try:
        cart = Cart(request)
        
        if request.POST.get('action') == 'post':
            product_id = request.POST.get('product_id')
            product_qty = request.POST.get("qty-cart")
            product = get_object_or_404(ProductDetail, id=product_id)
            cart.add(product=product,product_qty = product_qty)
            cart_qty = cart.__len__()
            return JsonResponse({"food": product.product_name, "qty": cart_qty})
    except Exception as e:
        logger.error(f"Error in cart_add: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)