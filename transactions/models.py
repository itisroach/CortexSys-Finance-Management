from django.db import models
from accounts.models import Account
from django.core.validators import MinValueValidator


class Transaction(models.Model):

    typeChoices = (("income", "income"), ("expense", "expense"))

    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, blank=False, null=False)
    amount = models.BigIntegerField(
        blank=False, null=False, validators=[MinValueValidator(1)]
    )

    type = models.CharField(max_length=10, choices=typeChoices, blank=False, null=False)

    date = models.DateField(blank=False, null=False)

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
