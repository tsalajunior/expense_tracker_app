from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.expenses.forms.expense import ExpenseForm
from apps.expenses.models import Expense


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "expenses/expense_list.html"
    context_object_name = "expenses"
    paginate_by = 10

    def get_queryset(self):
        return (
            Expense.objects
            .filter(user=self.request.user)
            .select_related("category", "payment_method")
        )

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_create.html"
    success_url = reverse_lazy("expenses:list")

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = "expenses/expense_detail.html"
    context_object_name = "expense"

    def get_queryset(self):
        return (
            Expense.objects
            .filter(user=self.request.user)
            .select_related("category", "payment_method")
        )


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_update.html"
    context_object_name = "expense"

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "expenses:detail",
            kwargs={"pk": self.object.pk},
        )


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = "expenses/expense_delete.html"
    context_object_name = "expense"
    success_url = reverse_lazy("expenses:list")

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)