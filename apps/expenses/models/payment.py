from django.db import models

from apps.core.models import BaseModel


class PaymentMethod(BaseModel):

    name = models.CharField(max_length=50, unique=True)

    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.name