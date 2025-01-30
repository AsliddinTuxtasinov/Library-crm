from django.db import models


class AuthStatusChoices(models.TextChoices):
    NEW = "new", "new"
    CODE_VERIFIED = "code_verified", "code_verified"
    DONE = "done", "done"


class AuthTypeChoices(models.TextChoices):
    VIA_EMAIL = "via_email", "via_email"
    VIA_PHONE = "via_phone", "via_phone"


class UserRolesChoices(models.TextChoices):
    ADMIN = 'admin', 'admin'
    OPERATOR = 'operator', 'operator'
    USER = 'user', 'user'


class UserSexChoices(models.IntegerChoices):
    MALE = 0, "male"
    FEMALE = 1, "female"
