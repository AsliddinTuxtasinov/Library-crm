import datetime

from django.utils import timezone
from rest_framework import generics, permissions, status, response, views, exceptions
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.ausers.enums import AuthTypeChoices, AuthStatusChoices
from apps.ausers.models import User, UserConfirmation
from apps.ausers.serializers import (
    LoginSerializers, LoginRegisterUserSerializers, ConfirmVerifyCodeSerializers, UpdateUserAuthSerializers,
    LoginRefreshSerializers
)
from apps.ausers.utils import error_response_message


class LoginRegisterUserViews(generics.GenericAPIView):
    serializer_class = LoginRegisterUserSerializers
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'auth_type': AuthTypeChoices.VIA_PHONE}
        )

        response_data = {"success": True}
        if user.auth_status == AuthStatusChoices.DONE:
            response_data.update({"status": 1})
        else:
            code, verify_code = user.create_verify_code(AuthTypeChoices.VIA_PHONE)
            # send_phone_code(user.phone_number, code)
            response_data.update({
                "status": 0,
                "expiration_time": verify_code.get_expiration_time_limit,
                "test_verify_code": code
            })

        return response.Response(status=status.HTTP_200_OK, data=response_data)


class ConfirmVerifyCodeView(generics.GenericAPIView):
    serializer_class = ConfirmVerifyCodeSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get('phone_number')
        code = serializer.validated_data.get('code')

        if not UserConfirmation.objects.filter(
                is_confirmed=False,
                expiration_time__gt=timezone.now(),
                code=code,
                user__phone_number=phone_number
        ).exists():
            raise exceptions.ValidationError("Verification code is invalid or expired")

        user_confirmation_obj = UserConfirmation.objects.get(
            is_confirmed=False,
            expiration_time__gt=timezone.now(),
            code=code,
            user__phone_number=phone_number
        )
        data = {
            "success": True,
            "token": user_confirmation_obj.user.token(),
        }
        user_confirmation_obj.is_confirmed = True
        user_confirmation_obj.save()

        return response.Response(status=status.HTTP_200_OK, data=data)


class UpdateUserAuthView(generics.UpdateAPIView):
    serializer_class = UpdateUserAuthSerializers
    permission_classes = [permissions.IsAuthenticated]

    # Method to get the object to be updated (the current authenticated user)
    def get_object(self):
        return self.request.user  # Return the current authenticated user as the object to be updated

    def update(self, request, *args, **kwargs):
        # Call the parent class's update method to perform the actual update
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return a response with a success message, updated user data, and authentication status
        return response.Response(
            data={
                "success": True,
                "message": "User updated successfully",
                "user": serializer.data,
                "auth_status": request.user.auth_status,
            },
            status=status.HTTP_200_OK
        )


class LoginViews(TokenObtainPairView):
    serializer_class = LoginSerializers


class GetNewVerificationCode(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        is_ok, response_data = self.check_verification_user(user)
        if not is_ok:
            return response.Response(data=response_data, status=status.HTTP_200_OK)

        if user.auth_type == AuthTypeChoices.VIA_PHONE:
            code, user_conf_obj = user.create_verify_code(AuthTypeChoices.VIA_PHONE)
            # we have not twilio account, so we use email
            # code = user.create_verify_code(VIA_PHONE)
            # send_phone_code(phone_number=user.phone_number, code=code)
            print(f"Verify code: {user.phone_number} -> code: {code}")
            return response.Response(data={
                "success": True,
                "err_msg": "Your new verification code is send !",
                "expiration_time": user_conf_obj.get_expiration_time_limit
            })

        else:
            error_response_message(
                message="Your phone number is incorrect !",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def check_verification_user(user):
        verify_code = user.verify_codes.filter(expiration_time__gt=timezone.now(), is_confirmed=False)
        if verify_code.exists():
            verify_code = verify_code.last()

            return False, {
                "success": False,
                "err_msg": "Your code is valid to use, please just wait a bit !",
                "expiration_time": verify_code.get_expiration_time_limit
            }

        return True, None


class LoginRefreshViews(TokenRefreshView):
    serializer_class = LoginRefreshSerializers
