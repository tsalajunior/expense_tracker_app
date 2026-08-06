from django.urls import path
from .views import UserLoginView, logout_view, UserRegisterView

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login",),
    path("register/", UserRegisterView.as_view(),name="register"),
    path("logout/", logout_view,name="logout",),
]