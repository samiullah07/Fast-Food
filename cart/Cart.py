from Products.models import ProductDetail

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("session_key")
        if "session_key" not in request.session:
            cart = self.session["session_key"] = {}
        self.cart = cart
        


    def add(self, product,product_qty):
        if product_qty is None or not product_qty.isdigit():
            product_qty = 1 
        
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {"price": str(product.prduct_price), "quantity": int(product_qty)}
        else:
            self.cart[product_id]["quantity"] = self.cart[product_id].get("quantity", 0) + int(product_qty)

        self.save()

    def __len__(self):
        return sum(item.get('quantity', 0) for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def get_prods(self):
        product_ids = self.cart.keys()
        products = ProductDetail.objects.filter(id__in=product_ids)
        return products
    
    def get_quantities(self):
        quantities = self.cart
        return quantities
    
    def cart_update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)
        ourcart = self.cart
        ourcart[product_id]["quantity"] = product_qty
        
        self.session.modified = True

        update_cart = self.cart
        return update_cart
        