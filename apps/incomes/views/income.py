from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.incomes.forms.income import IncomeForm
from apps.incomes.models import Income


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = "incomes/income_create.html"
    success_url = reverse_lazy("incomes:list")

    def form_valid(self, form):
        #The currently logged-in user should automatically become the owner of the revenue
        form.instance.user = self.request.user

        return super().form_valid(form)

class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = "incomes/income_list.html"
    context_object_name = "incomes"
    paginate_by = 10

    def get_queryset(self):
        return (
            Income.objects
            .filter(user=self.request.user)
            .select_related("category")
        )

class IncomeDetailView(LoginRequiredMixin, DetailView):
    model = Income
    template_name = "incomes/income_detail.html"
    context_object_name = "income"

    def get_queryset(self):
        return (
            Income.objects
            .filter(user=self.request.user)
            .select_related("category")
        )


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = "incomes/income_update.html"
    context_object_name = "income"

    def get_queryset(self):
        return Income.objects.filter(
            user=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy(
            "incomes:detail",
            kwargs={"pk": self.object.pk},
        )


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name = "incomes/income_delete.html"
    context_object_name = "income"
    success_url = reverse_lazy("incomes:list")

    def get_queryset(self):
        return Income.objects.filter(
            user=self.request.user
        )