from .Cart import Cart

# Create context processor so our cart can work on all pages of the site


def cart(request):
    cart = Cart(request)
    return {'cart': cart, 'cart_count': len(cart)}