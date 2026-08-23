from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from apps.alerts.models import Alert


class AlertListView(LoginRequiredMixin, ListView):
    model = Alert
    template_name = "alerts/alert_list.html"
    context_object_name = "alerts"
    paginate_by = 10

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user).order_by("-created_at")


class AlertMarkAsReadView(LoginRequiredMixin, View):

    def post(self, request, pk):

        alert = get_object_or_404(
            Alert,
            pk=pk,
            user=request.user,
        )

        if not alert.is_read:
            alert.is_read = True
            alert.save(update_fields=["is_read"])

            messages.success(
                request,
                "Alert marked as read.",
            )

        return redirect("alerts:list")


class AlertDeleteView(LoginRequiredMixin, DeleteView):

    model = Alert
    template_name = "alerts/alert_confirm_delete.html"
    success_url = reverse_lazy("alerts:list")

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)

    def form_valid(self, form):

        messages.success(
            self.request,
            "Alert deleted successfully.",
        )

        return super().form_valid(form)
