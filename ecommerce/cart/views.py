from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from products.models import Product
from .models import Cart, CartItem


class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        items_data = request.data.get("items", [])
        cart, created = Cart.objects.get_or_create(user=request.user)
        response_data = []

        for item_data in items_data:
            product_id = item_data.get("product_id")
            quantity = item_data.get("quantity", 1)
            size = item_data.get("size", None)
            color = item_data.get("color", None)


            if quantity <= 0:
                continue
            
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                response_data.append(
                    {"error": f"Product with ID {product_id} not found."}
                )
                continue

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, size=size, color=color
            )

            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()

            response_data.append(
                {
                    "id": cart_item.id,
                    "product": product.name,
                    "quantity": cart_item.quantity,
                    "total_cost": cart_item.get_total_cost(),
                    "selling_price_per_unit": product.selling_price,
                }
            )

        if any("error" in item for item in response_data):
            return Response(
                {
                    "message": "Some products could not be added to the cart.",
                    "data": response_data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Products added to cart successfully.", "data": response_data},
            status=status.HTTP_201_CREATED,
        )


class GetCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST
            )

        items = []
        total_cost = cart.get_total_cost()

        for item in cart.items.all():
            items.append(
                {
                    "id": item.id,  # Include the CartItem ID here
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "size": item.size,
                    "color": item.color,
                    "selling_price_per_unit": item.product.selling_price,
                    "total_cost": item.get_total_cost(),
                }
            )

        return Response(
            {
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                },
                "items": items,
                "grand_total": total_cost,
            }
        )


class RemoveItemFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        item_id = request.data.get("id")

        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)

            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

            else:
                cart_item.delete()

            total_cost = cart.get_total_cost()

            items = []
            for item in cart.items.all():
                items.append(
                    {
                        "id": item.id,
                        "product": item.product.name,
                        "quantity": item.quantity,
                        "size": item.size,
                        "color": item.color,
                        "selling_price_per_unit": item.product.selling_price,
                        "total_cost": item.get_total_cost(),
                    }
                )

            return Response(
                {
                    "message": "Item quantity updated or item removed from cart.",
                    "items": items,
                    "grand_total": total_cost,
                },
                status=status.HTTP_200_OK,
            )

        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found."}, status=status.HTTP_400_BAD_REQUEST
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found in cart."}, status=status.HTTP_400_BAD_REQUEST
            )
