from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """
    User login form.
    """

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Enter your username",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Enter your password",
            }
        ),
    )