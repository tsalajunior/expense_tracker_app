from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import CustomUser


class RegisterForm(UserCreationForm):
    """
    User registration form.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Enter your email",
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Choose a username",
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Create a password",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Confirm your password",
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )