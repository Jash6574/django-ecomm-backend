from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_cost(self):
        total_cost = sum(item.get_total_cost() for item in self.items.all())
        return total_cost


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    
    def get_total_cost(self):
        # Dynamically calculate the total cost
        return self.product.selling_price * self.quantity   
