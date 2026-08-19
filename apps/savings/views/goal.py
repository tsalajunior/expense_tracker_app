from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from apps.savings.forms import SavingsGoalForm
from apps.savings.models import SavingsGoal


class SavingsGoalCreateView(LoginRequiredMixin, CreateView):

    model = SavingsGoal
    form_class = SavingsGoalForm
    template_name = "savings/goals/goal_create.html"
    success_url = reverse_lazy("savings:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SavingsGoalListView(LoginRequiredMixin, ListView):

    model = SavingsGoal
    template_name = "savings/goals/goal_list.html"
    context_object_name = "savings_goals"

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


class SavingsGoalDetailView(LoginRequiredMixin, DetailView):

    model = SavingsGoal
    template_name = "savings/goals/goal_detail.html"
    context_object_name = "goal"

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


class SavingsGoalUpdateView(LoginRequiredMixin, UpdateView):

    model = SavingsGoal
    form_class = SavingsGoalForm
    template_name = "savings/goals/goal_update.html"
    context_object_name = "goal"

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse(
            "savings:detail",
            kwargs={
                "pk": self.object.pk,
            },
        )


class SavingsGoalDeleteView(LoginRequiredMixin, DeleteView):

    model = SavingsGoal
    template_name = "savings/goals/goal_delete.html"
    context_object_name = "goal"
    success_url = reverse_lazy("savings:list")

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)
