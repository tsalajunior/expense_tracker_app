from django.urls import path

from .views.expense import (
    ExpenseCreateView,
    ExpenseDeleteView,
    ExpenseDetailView,
    ExpenseListView,
    ExpenseUpdateView,
)


app_name = "expenses"


urlpatterns = [
    path("", ExpenseListView.as_view(), name="list"),
    path("create/", ExpenseCreateView.as_view(), name="create"),
    path("<int:pk>/",ExpenseDetailView.as_view(),name="detail",),
    path("<int:pk>/edit/",ExpenseUpdateView.as_view(),name="update",),
    path("<int:pk>/delete/",ExpenseDeleteView.as_view(),name="delete",),
]