from django.db import models
from django.contrib.auth.models import User
from Products.models import ProductDetail
from django.db.models.signals import post_save

# Create your models here.


class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Shipping Address"


    def __str__(self):
        return f"Payment of this user ! {self.user.id}"

# Create a user Profile by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
    if created:
       shipping_add =  ShippingAddress(user=instance)
       shipping_add.save()

# Connect signal after user is saved
post_save.connect(create_shipping, sender=User)




class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    shipping_address = models.TextField(max_length=1500)
    amount_paid = models.DecimalField(max_digits=7,decimal_places=2)
    order_dated = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Order - {str(self.id)}"
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(ProductDetail,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=1)


    def __str__(self):
        return f" Order Item - {str(self.id)}"
