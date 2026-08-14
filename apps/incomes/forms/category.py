from django import forms

from apps.incomes.models import IncomeCategory


class IncomeCategoryForm(forms.ModelForm):

    class Meta:
        model = IncomeCategory

        fields = [
            "name",
            "slug",
            "icon",
            "color",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Category name",
                }
            ),
            "slug": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "category-slug",
                }
            ),
            "icon": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Icon",
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Color",
                }
            ),
        }

        labels = {
            "name": "Name",
            "slug": "Slug",
            "icon": "Icon",
            "color": "Color",
        }