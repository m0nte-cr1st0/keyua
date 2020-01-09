# Django imports
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# Rest imports
from rest_framework import serializers

# Project imports
from project.inauth.models import PasswordResetRequest

User = get_user_model()


class AuthSerializer(serializers.Serializer):
    """
    Serializer for working with authentication for User.
    """
    name = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField()
    invite_key = serializers.CharField(required=False)
    package = serializers.CharField(required=False)
    period = serializers.CharField(required=False)


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for working with restore password for User.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email not found.")
        return value

    def apply_reset(self, email):
        password_request = PasswordResetRequest.generate_request(email=email)
        return password_request


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for working with resetting password.
    """
    password = serializers.CharField(required=True)
    password_repeat = serializers.CharField(required=True)
    key = serializers.CharField(required=True)

    def validate(self, data):
        """
        Check passwords are valid.
        """
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def validate_key(self, value):
        """
        Check key for reset request.
        """
        if not PasswordResetRequest.objects.filter(key=value, used=False).exists():
            raise serializers.ValidationError("Request key not found.")
        return value

    def validate_password(self, value):
        """
        Is the password valid? 
        """
        validate_password(value)
        return value
