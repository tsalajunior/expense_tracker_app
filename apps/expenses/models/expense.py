from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from .category import ExpenseCategory
from .payment import PaymentMethod


class Expense(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses",
    )

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name="expenses",
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
    )

    title = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    expense_date = models.DateField()

    description = models.TextField(blank=True)

    receipt = models.ImageField(
        upload_to="receipts/",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-expense_date"]

    def __str__(self):
        return f"{self.title} - {self.amount}"