from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]


class BankAccountType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    maximum_withdrawal_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    annual_interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00"))
        ],
        help_text="Interest rate from 0 to 100 percent"
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="How many times interest is calculated per year"
    )

    def calculate_interest(self, principal):
        principal = Decimal(principal)
        rate = self.annual_interest_rate
        periods = Decimal(self.interest_calculation_per_year)
        interest = principal * ((rate / Decimal("100.00")) / periods)
        return interest.quantize(Decimal("0.01"))

    def __str__(self):
        return self.name


class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name="bank_account",
        on_delete=models.CASCADE
    )
    account_type = models.ForeignKey(
        BankAccountType,
        related_name="accounts",
        on_delete=models.CASCADE
    )
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))]
    )
    interest_start_date = models.DateField(null=True, blank=True)
    initial_deposit_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def deposit(self, amount):
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self.balance += amount
        self.save()

        Transaction.objects.create(
            account=self,
            transaction_type="DEPOSIT",
            amount=amount,
            balance_after_transaction=self.balance,
            description="Deposit completed"
        )

    def withdraw(self, amount):
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if amount > self.account_type.maximum_withdrawal_amount:
            raise ValueError("Amount exceeds the maximum withdrawal limit for this account.")

        if amount > self.balance:
            raise ValueError("Insufficient balance.")

        self.balance -= amount
        self.save()

        Transaction.objects.create(
            account=self,
            transaction_type="WITHDRAWAL",
            amount=amount,
            balance_after_transaction=self.balance,
            description="Withdrawal completed"
        )

    def apply_interest(self):
        interest = self.account_type.calculate_interest(self.balance)
        self.balance += interest
        self.save()

        Transaction.objects.create(
            account=self,
            transaction_type="INTEREST",
            amount=interest,
            balance_after_transaction=self.balance,
            description="Interest applied"
        )

        return interest

    def __str__(self):
        return f"{self.user.username} - {self.account_no}"


class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name="address",
        on_delete=models.CASCADE
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.user.username} address"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
        ("INTEREST", "Interest"),
    ]

    account = models.ForeignKey(
        UserBankAccount,
        related_name="transactions",
        on_delete=models.CASCADE
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.account.account_no}"