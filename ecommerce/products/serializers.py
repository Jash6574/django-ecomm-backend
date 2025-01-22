from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, data):
        # Retrieve prices with default values
        selling_price = data.get("selling_price", None)
        actual_price = data.get("actual_price", None)

        # Validate short and long descriptions
        if len(data.get("short_description", "")) > 150:
            raise serializers.ValidationError(
                "Short description cannot exceed 150 characters."
            )
        if len(data.get("long_description", "")) > 1000:
            raise serializers.ValidationError(
                "Long description cannot exceed 1000 characters."
            )

        # Check discounted price logic
        if selling_price and actual_price and selling_price > actual_price:
            raise serializers.ValidationError(
                "Selling price cannot be greater than the actual price."
            )

        # Validate images
        if "images" in data:
            if len(data["images"]) < 1:
                raise serializers.ValidationError(
                    "You must upload at least 1 image."
                )
            if len(data["images"]) > 4:
                raise serializers.ValidationError(
                    "You can only upload a maximum of 4 images."
                )

        return data
