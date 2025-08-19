# users/models.py
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, name=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number must be set")
        phone_number = str(phone_number)
        user = self.model(phone_number=phone_number, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, name=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, name, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    phone_number = PhoneNumberField(unique=True, region="IR", null=False, blank=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def balance(self):
        income = (
            self.transaction_set.filter(type="income").aggregate(
                total=models.Sum("amount")
            )["total"]
            or 0
        )
        expense = (
            self.transaction_set.filter(type="expense").aggregate(
                total=models.Sum("amount")
            )["total"]
            or 0
        )

        return income - expense, income, expense


class DeviceToken(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="device_tokens"
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.token[:20]}"
