from decimal import Decimal

from django import forms
from django.utils import timezone

from apps.incomes.models import Income


class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income

        fields = [
            "category",
            "title",
            "amount",
            "income_date",
            "description",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Income title",
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

            "income_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                    "max": timezone.localdate().isoformat(),
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full p-3",
                    "placeholder": "Optional description...",
                    "rows": 4,
                }
            ),
        }

        labels = {
            "category": "Category",
            "title": "Title",
            "amount": "Amount",
            "income_date": "Date",
            "description": "Description",
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= Decimal("0.00"):
            raise forms.ValidationError(
                "The amount must be greater than 0."
            )

        return amount

    def clean_income_date(self):
        income_date = self.cleaned_data["income_date"]
        today = timezone.localdate()

        if income_date > today:
            raise forms.ValidationError(
                "The income date cannot be in the future. Correct the date."
            )

        return income_date