from django.urls import path

from apps.alerts.views import (
    AlertListView,
    AlertMarkAsReadView,
    AlertDeleteView,
)

app_name = "alerts"


urlpatterns = [
    path(
        "",
        AlertListView.as_view(),
        name="list",
    ),
    path(
        "<int:pk>/read/",
        AlertMarkAsReadView.as_view(),
        name="mark_as_read",
    ),
    path(
        "<int:pk>/delete/",
        AlertDeleteView.as_view(),
        name="delete",
    ),
]
