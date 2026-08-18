from django.urls import path
from apps.dashboard.views.dashboard import index
# from .views import index

app_name = "dashboard"

urlpatterns = [
    path("", index, name="dashboard"),
    # path("analytics/", analytics, name="analytics"),
    # path("reports/", reports, name="reports"),
]