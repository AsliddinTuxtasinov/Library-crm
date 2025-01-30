from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.ausers.models import User, UserConfirmation
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            _("Roles"),
            {
                "fields": (
                    "user_roles",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login",)
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone_number", "email", "first_name", "last_name", "is_staff", "user_roles")
    search_fields = ("first_name", "last_name", "email", "phone_number")
    ordering = ("-created_time", "phone_number",)


admin.site.register(User, UserAdmin)


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ["code", "verify_type", "user", "expiration_time", "is_confirmed"]
    list_filter = ["verify_type", "is_confirmed"]
