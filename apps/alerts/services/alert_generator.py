from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from apps.alerts.models import (
    Alert,
    AlertSeverity,
    AlertType,
)
from apps.budgets.models import Budget
from apps.expenses.models import Expense
from apps.savings.models import SavingsGoal


class AlertGenerator:

    @staticmethod
    def generate_for_user(user):
        """
        Generate all relevant alerts for a user.
        """

        AlertGenerator.generate_budget_alerts(user)
        AlertGenerator.generate_savings_goal_alerts(user)

    # =========================================================
    # BUDGET ALERTS
    # =========================================================

    @staticmethod
    def generate_budget_alerts(user):

        today = timezone.localdate()

        budgets = Budget.objects.filter(
            user=user,
            month=today.month,
            year=today.year,
        ).select_related("category")

        for budget in budgets:

            spent_amount = Expense.objects.filter(
                user=user,
                category=budget.category,
                expense_date__year=budget.year,
                expense_date__month=budget.month,
            ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

            # -------------------------------------------------
            # Budget exceeded
            # -------------------------------------------------

            if spent_amount > budget.amount:

                AlertGenerator.create_alert(
                    user=user,
                    alert_type=AlertType.BUDGET_EXCEEDED,
                    severity=AlertSeverity.DANGER,
                    title="Budget exceeded",
                    message=(
                        f"Your {budget.category.name} budget for "
                        f"{budget.month}/{budget.year} has been exceeded. "
                        f"Spent: {spent_amount:.2f} / "
                        f"Budget: {budget.amount:.2f}."
                    ),
                    budget=budget,
                )

            # -------------------------------------------------
            # Budget warning
            # -------------------------------------------------

            elif spent_amount >= budget.amount * Decimal("0.80"):

                AlertGenerator.create_alert(
                    user=user,
                    alert_type=AlertType.BUDGET_WARNING,
                    severity=AlertSeverity.WARNING,
                    title="Budget almost reached",
                    message=(
                        f"You have used at least 80% of your "
                        f"{budget.category.name} budget for "
                        f"{budget.month}/{budget.year}. "
                        f"Spent: {spent_amount:.2f} / "
                        f"Budget: {budget.amount:.2f}."
                    ),
                    budget=budget,
                )

    # =========================================================
    # SAVINGS GOAL ALERTS
    # =========================================================

    @staticmethod
    def generate_savings_goal_alerts(user):

        goals = SavingsGoal.objects.filter(
            user=user,
        )

        for goal in goals:

            # -------------------------------------------------
            # Goal completed
            # -------------------------------------------------

            if goal.is_completed:

                AlertGenerator.create_alert(
                    user=user,
                    alert_type=AlertType.SAVINGS_GOAL_COMPLETED,
                    severity=AlertSeverity.INFO,
                    title="Savings goal completed",
                    message=(
                        f"Congratulations! You have reached your "
                        f"savings goal '{goal.title}'."
                    ),
                    savings_goal=goal,
                )

            # -------------------------------------------------
            # Goal overdue
            # -------------------------------------------------

            elif goal.is_overdue:

                AlertGenerator.create_alert(
                    user=user,
                    alert_type=AlertType.SAVINGS_GOAL_OVERDUE,
                    severity=AlertSeverity.DANGER,
                    title="Savings goal overdue",
                    message=(
                        f"Your savings goal '{goal.title}' "
                        f"has passed its target date."
                    ),
                    savings_goal=goal,
                )

    # =========================================================
    # CREATE ALERT
    # =========================================================

    @staticmethod
    def create_alert(
        *,
        user,
        alert_type,
        severity,
        title,
        message,
        budget=None,
        savings_goal=None,
    ):
        """
        Create an alert only if the same business event
        does not already exist.
        """

        alert, created = Alert.objects.get_or_create(
            user=user,
            alert_type=alert_type,
            budget=budget,
            savings_goal=savings_goal,
            defaults={
                "severity": severity,
                "title": title,
                "message": message,
                "is_read": False,
            },
        )

        return alert, created
