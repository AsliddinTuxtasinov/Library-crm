from rest_framework import serializers

from apps.ausers.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email", "phone_number",
            "user_roles", "auth_type", "auth_status"
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "email"
            # "phone_number", "user_roles", "auth_type", "auth_status",
        ]
