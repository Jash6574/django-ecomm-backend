from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from orders.models import Orders, OrderItem


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        # Only superusers can access
        return request.user.is_authenticated and request.user.is_superuser


class RetrieveAllUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request):
        # Check authorization header
        print("Authorization header:", request.headers.get("Authorization"))
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to view this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )

        users = User.objects.all().values()  # Fetch users as dictionaries
        user_data = []

        for user_dict in users:
            user = User.objects.get(id=user_dict["id"])  # Get actual User object by ID
            orders = Orders.objects.filter(user=user)
            order_history = [
                {
                    "order_id": order.id,
                    "created_at": order.created_at,
                    "total_amount": order.total_amount,
                    "items": [
                        {
                            "product": item.product,  # You must access .name for product
                            "quantity": item.quantity,
                            "size": item.size,
                            "color": item.color,
                            "selling_price_per_unit": item.selling_price_per_unit,
                            "total_cost": item.total_cost,
                        }
                        for item in order.items.all()
                    ],
                }
                for order in orders
            ]

            # Add the order_history to the user dictionary
            user_info = {**user_dict, "order_history": order_history}
            user_data.append(user_info)

        return Response(user_data, status=status.HTTP_200_OK)


class RetrieveUserById(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    def get(self, request, id, *args, **kwargs):
        try:
            # Fetch the user using 'values' to get the data as a dictionary
            user_dict = User.objects.filter(id=id).values().first()  # Get first result as dictionary
            if not user_dict:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Fetch order history for this user
            orders = Orders.objects.filter(user_id=id)
            order_history = [
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
                            "selling_price_per_unit": item.selling_price_per_unit,
                            "total_cost": item.total_cost,
                        }
                        for item in order.items.all()
                    ],
                }
                for order in orders
            ]

            # Add the order history to the user dictionary
            user_data = {**user_dict, "order_history": order_history}

            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )