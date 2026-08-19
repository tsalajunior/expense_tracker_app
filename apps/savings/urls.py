from django.urls import path

from apps.savings.views import (
    SavingsGoalCreateView,
    SavingsGoalListView,
    SavingsGoalDetailView,
    SavingsGoalUpdateView,
    SavingsGoalDeleteView,
)

app_name = "savings"


urlpatterns = [
    path(
        "",
        SavingsGoalListView.as_view(),
        name="list",
    ),
    path(
        "create/",
        SavingsGoalCreateView.as_view(),
        name="create",
    ),
    path(
        "<int:pk>/",
        SavingsGoalDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/edit/",
        SavingsGoalUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/delete/",
        SavingsGoalDeleteView.as_view(),
        name="delete",
    ),
]
