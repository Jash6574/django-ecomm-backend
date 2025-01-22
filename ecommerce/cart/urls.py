from django.urls import path
from .views import AddToCart, GetCart, RemoveItemFromCart

urlpatterns = [
    path('add/', AddToCart.as_view(), name='add_to_cart'),
    path('', GetCart.as_view(), name='get_cart'),
    path('remove/', RemoveItemFromCart.as_view(), name='remove_from_cart'),
]
