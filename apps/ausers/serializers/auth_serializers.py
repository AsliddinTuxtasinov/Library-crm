from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers, exceptions, status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from apps.ausers.enums import AuthStatusChoices, AuthTypeChoices
from apps.ausers.models import User
from apps.ausers.utils import check_phone_number

# Constants for error messages
ERR_MSG_INVALID_INPUT = "You must enter a valid phone number, email, or username!"
ERR_MSG_PASSWORDS_NOT_MATCH = "Your passwords did not match!"
ERR_MSG_PASSWORDS_ARE_REQUIRED = "Password and confirm_password fields are required"
ERR_MSG_NOT_FULLY_REGISTERED = "You have not fully registered yet!"
ERR_MSG_INCORRECT_LOGIN_PASSWORD = "Sorry, the login or password you entered is incorrect. Please check and try again!"


class LoginRegisterUserSerializers(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    @staticmethod
    def validate_phone_number(value):
        if not check_phone_number(phone_number=value):
            raise serializers.ValidationError("Invalid input format")

        return value


class ConfirmVerifyCodeSerializers(LoginRegisterUserSerializers):
    code = serializers.CharField(required=True, min_length=4, max_length=4)


class UpdateUserAuthSerializers(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if not password or not confirm_password:
            raise exceptions.ValidationError(detail={"password and confirm_password": ERR_MSG_PASSWORDS_ARE_REQUIRED})

        if password != confirm_password:
            raise exceptions.ValidationError(detail={"password and confirm_password": ERR_MSG_PASSWORDS_NOT_MATCH})

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        if password:
            instance.set_password(password)
            instance.auth_status = AuthStatusChoices.DONE

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance


class LoginSerializers(TokenObtainPairSerializer, LoginRegisterUserSerializers):
    password = serializers.CharField(required=True, write_only=True)

    # Override username_field to use phone_number instead of username
    username_field = 'phone_number'

    def validate(self, attrs):
        # Validate user input and authenticate user
        user = self.auth_validate(attrs=attrs)
        data = user.token()
        data["auth_status"] = user.auth_status

        # Update last login if configured
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data

    def auth_validate(self, attrs):
        # Extract user input and password from attributes
        phone_number = str(attrs.get("phone_number")).lower()
        password = str(attrs.get("password"))

        # Retrieve user based on authentication type
        user = self.get_user(**{
            "phone_number": phone_number,
            "auth_type": AuthTypeChoices.VIA_PHONE
        })

        # Authenticate user using username and password
        user = authenticate(phone_number=user.phone_number, password=password)

        # Handle incorrect login credentials
        if user is not None:
            return user
        else:
            raise exceptions.ValidationError(ERR_MSG_INCORRECT_LOGIN_PASSWORD)

    @staticmethod
    def get_user(**kwargs):
        # Retrieve user from the database based on provided kwargs
        user_queryset = User.objects.filter(**kwargs)
        user = user_queryset.first()

        # Handle no active account found
        if user is None:
            raise exceptions.NotFound("No active account found!")
        return user


class LoginRefreshSerializers(TokenRefreshSerializer):
    # This custom serializer extends TokenRefreshSerializer to perform additional actions during token validation

    def validate(self, attrs):
        data = super().validate(attrs=attrs)  # Call the parent class's validate method and get the validated data
        access_token_instance = AccessToken(data['access'])  # Create an AccessToken instance from the access token

        user_id = access_token_instance['user_id']  # Extract the user ID from the access token's payload
        user = get_object_or_404(User, id=user_id)  # Get the user using the user ID, or raise a 404 if not found
        update_last_login(None, user)  # Assuming this function updates the user's last login time

        return data  # Return the validated data, including the access token
