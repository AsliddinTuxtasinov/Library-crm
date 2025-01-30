from rest_framework.permissions import BasePermission

from apps.ausers.enums import UserRolesChoices


class UserPermission(BasePermission):
    """
    Foydalanuvchi User yoki Admin rolida bo'lsa
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (
                    request.user.user_roles == UserRolesChoices.USER or
                    request.user.user_roles == UserRolesChoices.ADMIN
            )
        )


class UserAndOperatorPermission(BasePermission):
    """
    Foydalanuvchi User, Operator yoki Admin rolida bo'lsa
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (
                    request.user.user_roles == UserRolesChoices.USER or
                    request.user.user_roles == UserRolesChoices.OPERATOR or
                    request.user.user_roles == UserRolesChoices.ADMIN
            )
        )

    def has_object_permission(self, request, view, obj):

        if request.user.user_roles != UserRolesChoices.USER:
            return True

        return obj.user == request.user


class OperatorPermission(BasePermission):
    """
    Foydalanuvchi Operator yoki Admin rolida bo'lsa
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (
                    request.user.user_roles == UserRolesChoices.OPERATOR or
                    request.user.user_roles == UserRolesChoices.ADMIN
            )
        )
