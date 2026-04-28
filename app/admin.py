from django.contrib import admin
from .models import BankAccountType, UserBankAccount, UserAddress, Transaction


@admin.register(BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "maximum_withdrawal_amount",
        "annual_interest_rate",
        "interest_calculation_per_year",
    )


@admin.register(UserBankAccount)
class UserBankAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "account_no", "account_type", "balance", "created_at")
    search_fields = ("user__username", "account_no")


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "country")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "transaction_type",
        "amount",
        "balance_after_transaction",
        "created_at",
    )
    list_filter = ("transaction_type",)