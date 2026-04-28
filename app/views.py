from decimal import Decimal
import random

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import NewUserForm
from .models import UserBankAccount, BankAccountType


def home(request):
    return render(request, "app/index.html")


def accounts(request):
    return render(request, "app/accounts.html")


def planning(request):
    return render(request, "app/planning.html")


def service(request):
    return render(request, "app/service.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("app:dashboard")

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("app:dashboard")
        messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = NewUserForm()

    return render(request, "app/register.html", {"form": form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect("app:dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}.")
            return redirect("app:dashboard")
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "app/login.html", {"form": form})


@login_required
def logout_request(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect("app:home")

    return redirect("app:dashboard")


@login_required
def dashboard(request):
    account = (
        UserBankAccount.objects
        .filter(user=request.user)
        .select_related("account_type")
        .prefetch_related("transactions")
        .first()
    )

    return render(
        request,
        "app/dashboard.html",
        {
            "account": account
        },
    )


@login_required
def create_account(request):
    existing_account = UserBankAccount.objects.filter(user=request.user).first()
    if existing_account:
        messages.info(request, "You already have a bank account.")
        return redirect("app:dashboard")

    account_type = BankAccountType.objects.first()
    if not account_type:
        messages.error(
            request,
            "No bank account types are available yet. Please add one in the admin panel first."
        )
        return redirect("app:dashboard")

    account_number = random.randint(100000, 999999)
    while UserBankAccount.objects.filter(account_no=account_number).exists():
        account_number = random.randint(100000, 999999)

    UserBankAccount.objects.create(
        user=request.user,
        account_type=account_type,
        account_no=account_number
    )

    messages.success(request, "Your bank account has been created successfully.")
    return redirect("app:dashboard")


@login_required
@require_POST
def deposit(request):
    account = UserBankAccount.objects.filter(user=request.user).first()
    if not account:
        messages.error(request, "You need to create a bank account first.")
        return redirect("app:dashboard")

    amount = request.POST.get("amount", "").strip()

    try:
        account.deposit(Decimal(amount))
        messages.success(request, f"${Decimal(amount):.2f} deposited successfully.")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("app:dashboard")


@login_required
@require_POST
def withdraw(request):
    account = UserBankAccount.objects.filter(user=request.user).first()
    if not account:
        messages.error(request, "You need to create a bank account first.")
        return redirect("app:dashboard")

    amount = request.POST.get("amount", "").strip()

    try:
        account.withdraw(Decimal(amount))
        messages.success(request, f"${Decimal(amount):.2f} withdrawn successfully.")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("app:dashboard")