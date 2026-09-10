from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Public representation of a User — never includes the password hash."""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "date_joined"]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    # Public registration may only self-assign Consumer or Farmer — never Admin.
    role = serializers.ChoiceField(
        choices=[
            (User.Role.CONSUMER, User.Role.CONSUMER.label),
            (User.Role.FARMER, User.Role.FARMER.label),
        ],
        default=User.Role.CONSUMER,
    )

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role"]

    def validate_email(self, value):
        normalized = User.objects.normalize_email(value)
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return normalized

    def validate(self, attrs):
        user = User(
            email=attrs.get('email'),
            first_name=attrs.get('first_name', ''),
            last_name=attrs.get('last_name', ''),
        )

        try:
            validate_password(attrs['password'], user=user)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            email=attrs["email"],
            password=attrs["password"],
        )
        if user is None:
            # Deliberately generic — never reveal whether the email exists.
            raise serializers.ValidationError(
                "Unable to log in with the provided credentials.", code="authorization"
            )
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.", code="authorization")
        attrs["user"] = user
        return attrs