from django.db import models
from django.contrib.auth.models import User
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