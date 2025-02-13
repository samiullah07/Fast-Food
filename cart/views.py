from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .Cart import Cart
from Products.models import ProductDetail
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib import messages

def cart_summary(request):
    cart = Cart(request)

    products = cart.get_prods()
    total_price = 0  # Initialize the total price
    total_quantities = 0

    # Add calculated total price per product
    for product in products:
        product_id = str(product.id)

        if product.is_deal:
                product_price = float(product.deal_price)  # Ensure it's a float
                quantity = cart.cart.get(product_id, {}).get('quantity', 0)
                product.total_price = product_price * quantity  # Calculate total price for each product
                total_price += product.total_price  # Add to overall total price
                total_quantities += quantity
        else:
                product_price = float(product.prduct_price)  # Ensure it's a float
                quantity = cart.cart.get(product_id, {}).get('quantity', 0)
                product.total_price = product_price * quantity  # Calculate total price for each product
                total_price += product.total_price  # Add to overall total price
                total_quantities += quantity

   

    quantities = cart.get_quantities()

    context = {
        "products": products,
        "quantities": quantities,
        "total_price": total_price,
        "total_quantities" : total_quantities
    }

    return render(request, "cart.html", {"context": context})

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
            response = JsonResponse({"food": product.product_name, "qty": cart_qty})
            messages.success(request,"Product added to card successfully")
            return response
              
    except Exception as e:
        logger.error(f"Error in cart_add: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    


def update_cart(request):
    try:
        cart = Cart(request)
        
        if request.POST.get('action') == 'post':
            product_id = request.POST.get('product_id')
            product_qty = request.POST.get("product_qty")
            cart.cart_update(product=product_id,quantity=product_qty
)
            response = JsonResponse({"Quantity " : product_qty})
            messages.success(request,"Product Updated successfully")

            return response
              
    except Exception as e:
        logger.error(f"Error in cart_add: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    

def delete_item(request):
    
    try:
        cart = Cart(request)
        
        if request.POST.get('action') == 'post':
            product_id = request.POST.get('product_id')
            
           
            cart.delete_product(product=product_id)
            cart_qty = cart.__len__()

            response = JsonResponse({"response " : "Product deleted"})
            messages.success(request,"Product Deleted successfully")

            
            return response
              
    except Exception as e:
        logger.error(f"Error in cart_add: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
	
    