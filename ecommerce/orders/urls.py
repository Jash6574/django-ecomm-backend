from django.urls import path
from .views import Checkout,OrderHistory

urlpatterns = [
    path("checkout/", Checkout.as_view(), name="cart_checkout"),
    path("history/", OrderHistory.as_view(), name="order_history"),
]
