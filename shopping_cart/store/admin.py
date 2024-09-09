from django.contrib import admin
from .models import Cart,Product,CartItem

# Register your models here.
admin.site.register([Product, Cart, CartItem])