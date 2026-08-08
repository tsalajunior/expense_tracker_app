from decimal import Decimal

from django import forms

from apps.expenses.models import Expense


class ExpenseForm(forms.ModelForm):

    amount = forms.DecimalField(
        min_value=Decimal("0.01"),
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0.01",
            }
        ),
    )

    class Meta:
        model = Expense

        fields = [
            "category",
            "payment_method",
            "title",
            "amount",
            "expense_date",
            "description",
            "receipt",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "payment_method": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Expense title",
                }
            ),
            "expense_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full p-3",
                    "placeholder": "Optional description...",
                    "rows": 4,
                }
            ),
            "receipt": forms.ClearableFileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full",
                    "accept": "application/pdf",
                }
            ),
        }

        labels = {
            "category": "Category",
            "payment_method": "Payment method",
            "title": "Title",
            "amount": "Amount",
            "expense_date": "Date",
            "description": "Description",
            "receipt": "Receipt",
        }

        help_texts = {
            "receipt": "Optional. Upload your receipt in PDF format.",
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= 0:
            raise forms.ValidationError(
                "The amount must be greater than 0."
            )

        return amount