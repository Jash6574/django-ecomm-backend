from rest_framework import serializers
from django.contrib.auth.models import User
import re
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}
        
    def validate_password(self, value):
        errors = []

        # Check for minimum length (8 characters)
        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            errors.append("Password must contain at least one uppercase letter.")

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', value):
            errors.append("Password must contain at least one lowercase letter.")

        # Check for at least one digit
        if not re.search(r'\d', value):
            errors.append("Password must contain at least one number.")

        # Check for at least one special character
        if not re.search(r'[@$!%*?&]', value):
            errors.append("Password must contain at least one special character.")

        # If there are any errors, raise a validation error
        if errors:
            raise serializers.ValidationError(errors)

        return value

    def create(self, validated_data):
         # Custom validation for username and email uniqueness
        username = validated_data.get("username")
        email = validated_data.get("email")

         # Validate that the username is unique
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": ["A user with that username already exists."]})

        # Validate that the email is unique
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["A user with that email already exists."]})

        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation.pop("password", None)
        return representation


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
