from django.db import models
import uuid
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True



# Create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)  # Corrected this field
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.TextField(blank=True, null=True)  # Changed to TextField for larger data

    def __str__(self):
        return self.user.username


# Create a user Profile by default when user signs up
# This should already be present in your models.py
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # Ensure Profile is created

# Connect signal after user is saved
post_save.connect(create_profile, sender=User)




class Category(BaseModel):
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_name


class Customer(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=255)  # Passwords should be hashed, ensure this is managed securely
    profile_image = models.ImageField(upload_to="upload/profile", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name}"


class ProductDetail(BaseModel):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    product_des = models.TextField()
    prduct_price = models.IntegerField()
    product_image = models.ImageField(upload_to="upload/products")

    is_deal = models.BooleanField(default=False)
    deal_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name


class Order(BaseModel):
    productDetail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.IntegerField()  # Corrected this typo from 'quanitiy'
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.productDetail.product_name
