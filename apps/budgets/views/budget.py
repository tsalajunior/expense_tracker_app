from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from apps.budgets.forms.budget import BudgetForm
from apps.budgets.models import Budget


class BudgetCreateView(LoginRequiredMixin, CreateView):

    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_create.html"
    success_url = reverse_lazy("budgets:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user

        messages.success(
            self.request,
            "Budget created successfully.",
        )

        return super().form_valid(form)


class BudgetListView(LoginRequiredMixin, ListView):

    model = Budget
    template_name = "budgets/budget_list.html"
    context_object_name = "budgets"

    def get_queryset(self):
        return (
            Budget.objects.filter(user=self.request.user)
            .select_related("category")
            .order_by("-year", "-month", "category__name")
        )


class BudgetDetailView(LoginRequiredMixin, DetailView):

    model = Budget
    template_name = "budgets/budget_detail.html"
    context_object_name = "budget"

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related("category")


class BudgetUpdateView(LoginRequiredMixin, UpdateView):

    model = Budget
    form_class = BudgetForm
    template_name = "budgets/budget_update.html"
    context_object_name = "budget"

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related("category")

    def get_success_url(self):
        return reverse_lazy(
            "budgets:detail",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Budget updated successfully.",
        )

        return super().form_valid(form)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):

    model = Budget
    template_name = "budgets/budget_delete.html"
    context_object_name = "budget"

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).select_related("category")

    def get_success_url(self):
        return reverse_lazy("budgets:list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Budget deleted successfully.",
        )

        return super().form_valid(form)
