from django.contrib import admin
from .models import Product

# Register Product model with custom admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = (
        'name', 'category', 'subcategory', 'sku', 'stock', 'brand', 
        'selling_price', 'is_on_sale', 'rating'
    )
    
    # Allow filters for the admin list page
    list_filter = ('category', 'subcategory', 'brand', 'is_on_sale')
    
    # Add a search bar for filtering by name or description
    search_fields = ('name', 'short_description', 'long_description', 'sku')
    
    # Add the form fields to be used when adding or editing products in the admin interface
    fields = (
        'name', 'short_description', 'long_description', 'actual_price', 'selling_price',
        'category', 'subcategory', 'sku', 'stock', 'brand', 'tag', 'images', 'variants', 
        'is_on_sale', 'rating'
    )
    
 
