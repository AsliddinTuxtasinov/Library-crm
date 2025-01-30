import random
import uuid
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from rest_framework_simplejwt.tokens import RefreshToken

from apps.ausers.enums import AuthStatusChoices, AuthTypeChoices, UserRolesChoices
from apps.ausers.managers import CustomUserManager
from core.base.models import BaseModel


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), null=True, blank=True, unique=True)

    user_roles = models.CharField(max_length=35, choices=UserRolesChoices.choices, default=UserRolesChoices.USER)
    auth_type = models.CharField(max_length=35, choices=AuthTypeChoices.choices)
    auth_status = models.CharField(max_length=35, choices=AuthStatusChoices.choices, default=AuthStatusChoices.NEW)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0, 100) % 10) for _ in range(4)])
        user_conf_obj = UserConfirmation.objects.create(user_id=self.id, code=code, verify_type=verify_type)
        return code, user_conf_obj

    def check_email(self):
        if self.email:
            normalize_email = str(self.email).lower()  # Asliddin@gmail.com -> asliddin@gmail.com
            self.email = normalize_email

    def check_pass(self):
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def clean(self):
        self.check_email()
        self.check_pass()
        self.hashing_password()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'users'


# Define expiration times (in minutes) for phone and email verification codes
PHONE_EXPIRE = 1
EMAIL_EXPIRE = 5


# Define the UserConfirmation model
class UserConfirmation(BaseModel):
    # Fields for the UserConfirmation model
    # A field to store the verification code (assuming it's a 4-digit code)
    code = models.CharField(max_length=4)
    # A field to store verification type (email or phone)
    verify_type = models.CharField(max_length=35, choices=AuthTypeChoices.choices)
    # A foreign key to the related User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verify_codes")
    # A field to store the expiration time of the confirmation code
    expiration_time = models.DateTimeField(null=True)
    # A boolean field to indicate whether the user is confirmed or not
    is_confirmed = models.BooleanField(default=False)

    # Returns a string representation of the UserConfirmation instance (user's string representation)
    def __str__(self):
        return str(self.user.__str__())

    @property
    def get_expiration_time_limit(self):
        now_time = timezone.now()

        # Ensure expiration_time is timezone-aware
        if self.expiration_time and timezone.is_naive(self.expiration_time):
            self.expiration_time = timezone.make_aware(self.expiration_time, timezone.get_default_timezone())

        if not self.is_confirmed and self.expiration_time > now_time:
            time_diff = self.expiration_time - now_time
            return time_diff.total_seconds()

        return None

    def save(self, *args, **kwargs):
        # Calculate the expiration time based on the verification type chosen by the user
        # If verification type is email, set the expiration time as current time + EMAIL_EXPIRE minutes
        if self.verify_type == AuthTypeChoices.VIA_EMAIL:
            expiration_time = datetime.now() + timedelta(minutes=EMAIL_EXPIRE)
        else:
            # If verification type is phone, set the expiration time as current time + PHONE_EXPIRE minutes
            expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        # Assign the calculated expiration time to the model instance
        self.expiration_time = expiration_time

        # Call the parent class's save method to save the model instance in the database
        super().save(*args, **kwargs)
