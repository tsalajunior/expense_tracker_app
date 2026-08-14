from django.urls import path

from apps.incomes.views.income import (
    IncomeCreateView,
    IncomeDeleteView,
    IncomeDetailView,
    IncomeListView,
    IncomeUpdateView,
)

from apps.incomes.views.category import (
    IncomeCategoryListView,
    IncomeCategoryCreateView,
    IncomeCategoryDetailView,
    IncomeCategoryUpdateView,
    IncomeCategoryDeleteView,
)

app_name = "incomes"

urlpatterns = [
    path("", IncomeListView.as_view(), name="list"),
    path("create/", IncomeCreateView.as_view(), name="create"),
    path(
        "<int:pk>/",
        IncomeDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/update/",
        IncomeUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/delete/",
        IncomeDeleteView.as_view(),
        name="delete",
    ),
    path(
        "categories/",
        IncomeCategoryListView.as_view(),
        name="category_list",
    ),
    path(
        "categories/create/",
        IncomeCategoryCreateView.as_view(),
        name="category_create",
    ),
    path(
        "categories/<int:pk>/",
        IncomeCategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "categories/<int:pk>/update/",
        IncomeCategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "categories/<int:pk>/delete/",
        IncomeCategoryDeleteView.as_view(),
        name="category_delete",
    ),
]
