from django.urls import path
from apps.budgets.views import (
    BudgetCreateView,
    BudgetListView,
    BudgetDetailView,
    BudgetUpdateView,
    BudgetDeleteView,
)

app_name = "budgets"

urlpatterns = [
    path(
        "",
        BudgetListView.as_view(),
        name="list",
    ),
    path(
        "create/",
        BudgetCreateView.as_view(),
        name="create",
    ),
    path(
        "<int:pk>/",
        BudgetDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/update/",
        BudgetUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/delete/",
        BudgetDeleteView.as_view(),
        name="delete",
    ),
]
