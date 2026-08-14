from django.urls import path

from .views.expense import (
    ExpenseCreateView,
    ExpenseDeleteView,
    ExpenseDetailView,
    ExpenseListView,
    ExpenseUpdateView,
)
from apps.expenses.views.category import (
    ExpenseCategoryListView,
    ExpenseCategoryCreateView,
    ExpenseCategoryDetailView,
    ExpenseCategoryUpdateView,
    ExpenseCategoryDeleteView,
)

app_name = "expenses"


urlpatterns = [
    path("", ExpenseListView.as_view(), name="list"),
    path("create/", ExpenseCreateView.as_view(), name="create"),
    path(
        "<int:pk>/",
        ExpenseDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/edit/",
        ExpenseUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/delete/",
        ExpenseDeleteView.as_view(),
        name="delete",
    ),
    path(
        "categories/",
        ExpenseCategoryListView.as_view(),
        name="category_list",
    ),
    path(
        "categories/create/",
        ExpenseCategoryCreateView.as_view(),
        name="category_create",
    ),
    path(
        "categories/<int:pk>/",
        ExpenseCategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "categories/<int:pk>/update/",
        ExpenseCategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "categories/<int:pk>/delete/",
        ExpenseCategoryDeleteView.as_view(),
        name="category_delete",
    ),
]
