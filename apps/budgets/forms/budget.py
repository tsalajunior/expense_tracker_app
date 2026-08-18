from decimal import Decimal

from django import forms

from apps.budgets.models import Budget
from apps.expenses.models import ExpenseCategory


class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget

        fields = [
            "category",
            "amount",
            "month",
            "year",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "amount": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
            "month": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "year": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "2026",
                    "min": "2000",
                    "step": "1",
                }
            ),
        }

        labels = {
            "category": "Expense category",
            "amount": "Monthly budget",
            "month": "Month",
            "year": "Year",
        }

        help_texts = {
            "amount": "Enter the maximum amount you plan to spend for this category.",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        # Only display expense categories.
        self.fields["category"].queryset = ExpenseCategory.objects.all()

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= Decimal("0.00"):
            raise forms.ValidationError("The budget amount must be greater than 0.")

        return amount

    def clean_year(self):
        year = self.cleaned_data["year"]

        if year < 2000:
            raise forms.ValidationError("Please enter a valid year.")

        return year

    def clean(self):
        cleaned_data = super().clean()

        category = cleaned_data.get("category")
        month = cleaned_data.get("month")
        year = cleaned_data.get("year")

        if self.user and category and month and year:
            existing_budget = Budget.objects.filter(
                user=self.user,
                category=category,
                month=month,
                year=year,
            )

            # When editing, don't consider the current object
            # as a duplicate.
            if self.instance.pk:
                existing_budget = existing_budget.exclude(pk=self.instance.pk)

            if existing_budget.exists():
                raise forms.ValidationError(
                    "A budget already exists for this category and month."
                )

        return cleaned_data
