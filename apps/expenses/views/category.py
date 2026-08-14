from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.expenses.forms.category import ExpenseCategoryForm
from apps.expenses.models import ExpenseCategory


class ExpenseCategoryListView(LoginRequiredMixin, ListView):
    model = ExpenseCategory
    template_name = "expenses/categories/category_list.html"
    context_object_name = "categories"


class ExpenseCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/categories/category_create.html"
    success_url = reverse_lazy("expenses:category_list")


class ExpenseCategoryDetailView(LoginRequiredMixin, DetailView):
    model = ExpenseCategory
    template_name = "expenses/categories/category_detail.html"
    context_object_name = "category"


class ExpenseCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseCategory
    form_class = ExpenseCategoryForm
    template_name = "expenses/categories/category_update.html"
    context_object_name = "category"

    def get_success_url(self):
        return reverse_lazy(
            "expenses:category_detail",
            kwargs={"pk": self.object.pk},
        )


class ExpenseCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = ExpenseCategory
    template_name = "expenses/categories/category_delete.html"
    context_object_name = "category"
    success_url = reverse_lazy("expenses:category_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            return super().post(request, *args, **kwargs)

        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{self.object.name}" because it is '
                f'currently used by existing expenses.'
            )

            return redirect(
                "expenses:category_detail",
                pk=self.object.pk,
            )