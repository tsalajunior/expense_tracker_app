from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class AlertType(models.TextChoices):

    BUDGET_WARNING = (
        "budget_warning",
        "Budget Almost Reached",
    )

    BUDGET_EXCEEDED = (
        "budget_exceeded",
        "Budget Exceeded",
    )

    SAVINGS_GOAL_COMPLETED = (
        "savings_goal_completed",
        "Savings Goal Completed",
    )

    SAVINGS_GOAL_OVERDUE = (
        "savings_goal_overdue",
        "Savings Goal Overdue",
    )


class AlertSeverity(models.TextChoices):

    INFO = (
        "info",
        "Information",
    )

    WARNING = (
        "warning",
        "Warning",
    )

    DANGER = (
        "danger",
        "Danger",
    )


class Alert(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="alerts",
    )

    alert_type = models.CharField(
        max_length=50,
        choices=AlertType.choices,
    )

    severity = models.CharField(
        max_length=20,
        choices=AlertSeverity.choices,
        default=AlertSeverity.INFO,
    )

    title = models.CharField(
        max_length=200,
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False,
    )

    budget = models.ForeignKey(
        "budgets.Budget",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="alerts",
    )

    savings_goal = models.ForeignKey(
        "savings.SavingsGoal",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="alerts",
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Alert"
        verbose_name_plural = "Alerts"

    def __str__(self):

        return self.title
