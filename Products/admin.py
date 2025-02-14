from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Category)
admin.site.register(ProductDetail)
admin.site.register(Order)
admin.site.register(Customer)

class ProfileInlines(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username","first_name","last_name","email"]
    inlines = [ProfileInlines]


admin.site.unregister(User)


admin.site.register(User,UserAdmin)
admin.site.register(Profile)