from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=150)
    long_description = models.CharField(max_length=1000)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)
    stock = models.PositiveIntegerField()
    brand = models.CharField(max_length=100)
    tag = models.TextField()
    images = models.JSONField()
    variants = models.JSONField()
    is_on_sale = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

