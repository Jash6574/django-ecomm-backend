from django.urls import path
from .views import AddProduct, GetAllProducts, GetProductById, UpdateProduct, DeleteProduct

urlpatterns = [
    path('add/', AddProduct.as_view(), name='add_product'),
    path('all/', GetAllProducts.as_view(), name='get_all_products'),
    path('<int:id>/', GetProductById.as_view(), name='get_product_by_id'),
    path('update/<int:id>/', UpdateProduct.as_view(), name='update_product'),
    path('delete/<int:id>/', DeleteProduct.as_view(), name='delete_product'),

]
