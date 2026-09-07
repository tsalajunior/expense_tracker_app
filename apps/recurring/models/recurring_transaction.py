from datetime import date
import calendar

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.expenses.models.category import ExpenseCategory
from apps.expenses.models.payment import PaymentMethod
from apps.incomes.models.category import IncomeCategory


class RecurringTransaction(BaseModel):
    """
    Represents a transaction that is automatically generated
    according to a defined frequency.
    """

    class TransactionType(models.TextChoices):
        EXPENSE = "expense", "Expense"
        INCOME = "income", "Income"

    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recurring_transactions",
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )

    title = models.CharField(
        max_length=200,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # Used only for recurring expenses
    expense_category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name="recurring_transactions",
        null=True,
        blank=True,
    )

    # Used only for recurring incomes
    income_category = models.ForeignKey(
        IncomeCategory,
        on_delete=models.PROTECT,
        related_name="recurring_transactions",
        null=True,
        blank=True,
    )

    # Expenses require a payment method.
    # Incomes do not have one in the current project.
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        related_name="recurring_transactions",
        null=True,
        blank=True,
    )

    frequency = models.CharField(
        max_length=10,
        choices=Frequency.choices,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    next_run_date = models.DateField(
        null=True,
        blank=True,
    )

    last_generated_date = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["next_run_date", "-created_at"]

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(
                        transaction_type="expense",
                        expense_category__isnull=False,
                        income_category__isnull=True,
                        payment_method__isnull=False,
                    )
                    | models.Q(
                        transaction_type="income",
                        expense_category__isnull=True,
                        income_category__isnull=False,
                        payment_method__isnull=True,
                    )
                ),
                name="valid_recurring_transaction_type",
            ),
        ]

        verbose_name = "Recurring Transaction"
        verbose_name_plural = "Recurring Transactions"

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.frequency})"

    def clean(self):
        """
        Validate the business rules of a recurring transaction.
        """

        errors = {}

        # ---------------------------------------------------------
        # Amount
        # ---------------------------------------------------------
        if self.amount is not None and self.amount <= 0:
            errors["amount"] = "Amount must be greater than zero."

        # ---------------------------------------------------------
        # Dates
        # ---------------------------------------------------------
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                errors["end_date"] = "End date cannot be earlier than start date."

        if self.next_run_date and self.start_date:
            if self.next_run_date < self.start_date:
                errors["next_run_date"] = (
                    "Next run date cannot be earlier than start date."
                )

        if self.last_generated_date and self.start_date:
            if self.last_generated_date < self.start_date:
                errors["last_generated_date"] = (
                    "Last generated date cannot be earlier than start date."
                )

        if self.end_date and self.next_run_date and self.next_run_date > self.end_date:
            errors["next_run_date"] = "Next run date cannot be later than the end date."

        if (
            self.last_generated_date
            and self.next_run_date
            and self.last_generated_date > self.next_run_date
        ):
            errors["last_generated_date"] = (
                "Last generated date cannot be later than next run date."
            )

        # ---------------------------------------------------------
        # Expense-specific validation
        # ---------------------------------------------------------
        if self.transaction_type == self.TransactionType.EXPENSE:

            if not self.expense_category:
                errors["expense_category"] = (
                    "An expense category is required for an expense."
                )

            if self.income_category:
                errors["income_category"] = (
                    "Income category cannot be used for an expense."
                )

            if not self.payment_method:
                errors["payment_method"] = (
                    "A payment method is required for an expense."
                )

        # ---------------------------------------------------------
        # Income-specific validation
        # ---------------------------------------------------------
        elif self.transaction_type == self.TransactionType.INCOME:

            if not self.income_category:
                errors["income_category"] = (
                    "An income category is required for an income."
                )

            if self.expense_category:
                errors["expense_category"] = (
                    "Expense category cannot be used for an income."
                )

            if self.payment_method:
                errors["payment_method"] = (
                    "Payment method cannot be used for an income."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Automatically initialize next_run_date with start_date
        when it has not been provided.
        """

        if self.next_run_date is None and self.start_date:
            self.next_run_date = self.start_date

        super().save(*args, **kwargs)

    def calculate_next_run_date(self, current_date=None):
        """
        Calculate the next execution date according to the frequency.

        Handles month-end correctly:
        January 31 -> February 28/29
        March 31 -> April 30
        """

        current_date = current_date or self.next_run_date

        if current_date is None:
            raise ValueError(
                "next_run_date must be set before calculating the next date."
            )

        if self.frequency == self.Frequency.DAILY:
            from datetime import timedelta

            return current_date + timedelta(days=1)

        if self.frequency == self.Frequency.WEEKLY:
            from datetime import timedelta

            return current_date + timedelta(weeks=1)

        if self.frequency == self.Frequency.MONTHLY:
            year = current_date.year
            month = current_date.month

            # Move to the next month
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1

            # Preserve the original day when possible.
            # Otherwise use the last day of the target month.
            last_day = calendar.monthrange(year, month)[1]
            day = min(current_date.day, last_day)

            return date(year, month, day)

        if self.frequency == self.Frequency.YEARLY:
            try:
                return current_date.replace(year=current_date.year + 1)
            except ValueError:
                # February 29 -> February 28 in a non-leap year
                return current_date.replace(
                    year=current_date.year + 1,
                    day=28,
                )

        raise ValueError(f"Unsupported frequency: {self.frequency}")

    def advance_next_run_date(self):
        """
        Move next_run_date to the next scheduled date.
        """

        if self.next_run_date is None:
            self.next_run_date = self.start_date
        else:
            self.next_run_date = self.calculate_next_run_date()

        return self.next_run_date

    def is_due(self, current_date=None):
        """
        Return True when the recurring transaction should be generated.
        """

        current_date = current_date or date.today()

        if not self.is_active:
            return False

        if self.next_run_date is None:
            return False

        if self.end_date and self.next_run_date > self.end_date:
            return False

        return self.next_run_date <= current_date

    def deactivate_if_expired(self):
        """
        Automatically deactivate the recurring transaction
        when its end date has been reached.
        """

        if self.end_date and self.next_run_date and self.next_run_date > self.end_date:
            self.is_active = False
            return True

        return False
