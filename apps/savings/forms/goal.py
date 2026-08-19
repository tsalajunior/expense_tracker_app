from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.savings.models import SavingsGoal


class SavingsGoalForm(forms.ModelForm):

    class Meta:
        model = SavingsGoal

        fields = [
            "title",
            "target_amount",
            "saved_amount",
            "target_date",
            "description",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. New Laptop",
                }
            ),
            "target_amount": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. 100000",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
            "saved_amount": forms.NumberInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "e.g. 25000",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "target_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "placeholder": "Describe your savings goal...",
                    "rows": 4,
                }
            ),
        }

    def clean_target_date(self):
        target_date = self.cleaned_data["target_date"]

        if target_date < timezone.localdate():
            raise ValidationError("The target date cannot be in the past.")

        return target_date

    def clean(self):
        cleaned_data = super().clean()

        target_amount = cleaned_data.get("target_amount")
        saved_amount = cleaned_data.get("saved_amount")

        if (
            target_amount is not None
            and saved_amount is not None
            and saved_amount > target_amount
        ):
            raise ValidationError(
                "Saved amount cannot be greater than the target amount."
            )

        return cleaned_data
