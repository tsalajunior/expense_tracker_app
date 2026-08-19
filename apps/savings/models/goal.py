from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import BaseModel


class SavingsGoal(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="savings_goals",
    )

    title = models.CharField(
        max_length=200,
    )

    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )

    saved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
        ],
    )

    target_date = models.DateField()

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["target_date", "-created_at"]
        verbose_name = "Savings Goal"
        verbose_name_plural = "Savings Goals"

    def __str__(self):
        return self.title

    @property
    def remaining_amount(self):
        return max(
            self.target_amount - self.saved_amount,
            Decimal("0.00"),
        )

    @property
    def progress_percentage(self):
        if self.target_amount <= 0:
            return Decimal("0.00")

        progress = (self.saved_amount / self.target_amount) * Decimal("100")

        return min(progress, Decimal("100.00"))

    @property
    def is_completed(self):
        return self.saved_amount >= self.target_amount

    @property
    def is_overdue(self):
        if self.is_completed:
            return False

        from django.utils import timezone

        return self.target_date < timezone.localdate()
