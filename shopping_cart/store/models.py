from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    picture = models.ImageField(upload_to='img',default='')

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.uuid)
    
    @property
    def total_price(self):
        cartitems = self.cartitems.all()
        total = sum(item.price for item in cartitems)
        return total
    
    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum(item.quantity for item in cartitems)
        return quantity
    
class CartItem(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.products.name
    
    @property
    def price(self):
        sum_price = self.products.price * self.quantity
        return sum_price
    
    