from django.urls import path

from apps.incomes.views.income import (
    IncomeCreateView,
    IncomeDeleteView,
    IncomeDetailView,
    IncomeListView,
    IncomeUpdateView,
)

app_name = "incomes"

urlpatterns = [
    path("", IncomeListView.as_view(), name="list"),
    path("create/", IncomeCreateView.as_view(), name="create"),
    path("<int:pk>/", IncomeDetailView.as_view(), name="detail",),
    path("<int:pk>/update/", IncomeUpdateView.as_view(), name="update",),
    path("<int:pk>/delete/", IncomeDeleteView.as_view(), name="delete",),
]