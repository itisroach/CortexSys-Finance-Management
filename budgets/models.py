from django.db import models
from accounts.models import Account
from django.core.validators import MinValueValidator

class Budget(models.Model):

    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=False, blank=False)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False, validators=[MinValueValidator(1)])

    start_date = models.DateField(null=False, blank=False)

    end_date = models.DateField(null=False, blank=False)


    def spent_amount(self):
        return self.user_id.transaction_set.filter(
            type="expense",
            date__range=(self.start_date, self.end_date)
        ).aggregate(total=models.Sum("amount"))["total"] or 0


    def check_limit(self, added_amount):
        spent = self.spent_amount() + added_amount
        if spent > self.total_amount:
            return f"Budget '{self.title}' exceeded! Limit: {self.total_amount}, Spent: {spent}"

    def __str__(self):
        return self.title
