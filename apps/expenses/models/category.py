from django.db import models

from apps.core.models import BaseModel


class ExpenseCategory(BaseModel):

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(unique=True)

    icon = models.CharField(max_length=50, blank=True,)

    color = models.CharField(max_length=20, blank=True,)

    class Meta:
        ordering = ["name"]
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"

    def __str__(self):
        return self.name