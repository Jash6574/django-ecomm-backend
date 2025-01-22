from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Orders, OrderItem
from cart.models import Cart, CartItem
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Retrieve the cart for the logged-in user
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()

            if not cart_items.exists():
                return Response(
                    {"error": "Cart is empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Calculate the total cost of the cart
            total_amount = sum(item.get_total_cost() for item in cart_items)

            # Create a new order for the user
            order = Orders.objects.create(user=request.user, total_amount=total_amount)

            # Add cart items to the order
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product.name,
                    quantity=item.quantity,
                    size=item.size,
                    color=item.color,
                    selling_price_per_unit=item.product.selling_price,
                    total_cost=item.get_total_cost(),
                )

            # Create a Stripe Checkout session
            line_items = [
                {
                    "price_data": {
                        "currency": "inr",
                        "product_data": {
                            "name": item.product.name,
                        },
                        "unit_amount": int(item.product.selling_price * 100),
                    },
                    "quantity": item.quantity,
                }
                for item in cart_items
            ]

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url="http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://127.0.0.1:8000/cancel",
                shipping_address_collection={
                    "allowed_countries": ["IN"],  
                },
                
                customer_email=request.user.email,  
                metadata={  
                    "order_id": order.id,
                }
            )

            # Clear the cart
            cart.items.all().delete()

            # Respond with the Stripe session URL
            return Response(
                {
                    "message": "Checkout initiated successfully!",
                    "order_id": order.id,
                    "total_amount": total_amount,
                    "checkout_url": session.url,  # URL to redirect the user to the payment page
                },
                status=status.HTTP_201_CREATED,
            )

        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found."}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OrderHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Orders.objects.filter(user=request.user).order_by("-created_at")
        order_data = [
            {
                "order_id": order.id,
                "created_at": order.created_at,
                "total_amount": order.total_amount,
                "items": [
                    {
                        "product": item.product,
                        "quantity": item.quantity,
                        "size": item.size,
                        "color": item.color,
                        "price_per_unit": item.selling_price_per_unit,
                        "total_cost": item.total_cost,
                    }
                    for item in order.items.all()
                ],
            }
            for order in orders
        ]

        return Response(order_data, status=status.HTTP_200_OK)
