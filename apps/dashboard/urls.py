from django.urls import path

from .views import index

app_name = "dashboard"

urlpatterns = [
    path("", index, name="index"),
    # path("analytics/", analytics, name="analytics"),
    # path("reports/", reports, name="reports"),
]