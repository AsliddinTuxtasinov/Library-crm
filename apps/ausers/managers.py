import re

from django.contrib.auth.base_user import BaseUserManager

from apps.ausers.enums import UserRolesChoices


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError('The phone_number must be set')

        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number=phone_number, password=password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_roles', UserRolesChoices.ADMIN)
        return self._create_user(phone_number=phone_number, password=password, **extra_fields)

    @classmethod
    def normalize_phone_number(cls, phone_number, default_country_code="998"):
        """
        Normalize a phone number to an international format (E.164 standard) without external libraries.

        Args:
            phone_number (str): The phone number to normalize.
            default_country_code (str): The default country code to use if not present.

        Returns:
            str: The normalized phone number in E.164 format, or None if invalid.
        """
        phone_number = phone_number or ""
        # Remove non-numeric characters
        phone_number = re.sub(r"\D", "", phone_number)

        # Check if the phone number starts with a "+"
        if phone_number.startswith("00"):  # Convert "00" prefix to "+"
            phone_number = "+" + phone_number[2:]
        elif phone_number.startswith("+"):
            phone_number = phone_number
        elif phone_number.startswith(default_country_code):
            phone_number = "+" + phone_number
        else:
            # Assume the phone number is missing a country code
            phone_number = "+" + default_country_code + phone_number.lstrip("0")

        # Validate length (E.164 format allows up to 15 digits, including country code)
        if len(phone_number) > 20 or not phone_number.startswith("+"):
            return None  # Invalid phone number

        return phone_number
