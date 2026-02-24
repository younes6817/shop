from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from shop import settings


class UserManager(BaseUserManager):
    def create_user(self, phone=None, password=None, **extra_fields):
        email = extra_fields.get("email")
        if not phone and not email:
            raise ValueError("حداقل یکی از شماره تلفن یا ایمیل الزامی است.")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("ادمین باید is_staff=True باشد")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("ادمین باید is_superuser=True باشد")

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None

    phone = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(regex=r"^09\d{9}$")],
    )

    role = models.CharField(max_length=20, choices=settings.base.USER_ROLE, default="customer")
    point = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone or self.email or str(self.pk)

