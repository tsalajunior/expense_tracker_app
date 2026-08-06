from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib import messages
from django.views.generic import CreateView
from apps.accounts.forms import LoginForm
from apps.accounts.forms import RegisterForm
from apps.accounts.models import CustomUser


class UserLoginView(LoginView):
    """
    Handle user authentication.
    """

    form_class = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard:index")


@login_required
def logout_view(request):
    """
    Log out the current user.
    """

    logout(request)

    return redirect("accounts:login")


class UserRegisterView(CreateView):
    """
    Handle user registration.
    """

    model = CustomUser
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your account has been created successfully. You can now sign in.",
        )
        return super().form_valid(form)


    