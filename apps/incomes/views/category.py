from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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

from apps.incomes.forms.category import IncomeCategoryForm
from apps.incomes.models import IncomeCategory


class IncomeCategoryListView(LoginRequiredMixin, ListView):
    model = IncomeCategory
    template_name = "incomes/categories/category_list.html"
    context_object_name = "categories"


class IncomeCategoryCreateView(LoginRequiredMixin, CreateView):
    model = IncomeCategory
    form_class = IncomeCategoryForm
    template_name = "incomes/categories/category_create.html"
    success_url = reverse_lazy("incomes:category_list")


class IncomeCategoryDetailView(LoginRequiredMixin, DetailView):
    model = IncomeCategory
    template_name = "incomes/categories/category_detail.html"
    context_object_name = "category"


class IncomeCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = IncomeCategory
    form_class = IncomeCategoryForm
    template_name = "incomes/categories/category_update.html"
    context_object_name = "category"

    def get_success_url(self):
        return reverse_lazy(
            "incomes:category_detail",
            kwargs={"pk": self.object.pk},
        )


class IncomeCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = IncomeCategory
    template_name = "incomes/categories/category_delete.html"
    context_object_name = "category"
    success_url = reverse_lazy("incomes:category_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            return super().post(request, *args, **kwargs)

        except ProtectedError:
            messages.error(
                request,
                f'Cannot delete "{self.object.name}" because it is '
                f"currently used by existing incomes.",
            )

            return redirect(
                "incomes:category_detail",
                pk=self.object.pk,
            )