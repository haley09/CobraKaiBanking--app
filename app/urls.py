from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("accounts/", views.accounts, name="accounts"),
    path("planning/", views.planning, name="planning"),
    path("service/", views.service, name="service"),

    path("register/", views.register, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("create-account/", views.create_account, name="create_account"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
]