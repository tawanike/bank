from django.db import models
from django.contrib.auth.models import User

from bank.accounts.models import Account

class Transaction(models.Model):
  DEPOSIT = 0
  WITHDRAWAL = 1

  TRANSACTION_TYPE_CHOICES = (
    (DEPOSIT, 'Deposit'),
    (WITHDRAWAL, 'Withdrawal'),
  )

  ATM = 0
  BRANCH = 1
  EFT = 2

  TRANSACTION_SOURCE_CHOICES = (
    (ATM, 'ATM'),
    (BRANCH, 'Branch'),
    (EFT, 'EFT'),
  )

  user = models.ForeignKey(User, blank=True, null=True, related_name='transactions', on_delete=models.CASCADE)
  old_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
  new_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
  transaction_type = models.IntegerField(default=DEPOSIT, choices=TRANSACTION_TYPE_CHOICES)
  amount = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
  reference = models.CharField(max_length=255, null=True, blank=True)
  from_account = models.ForeignKey(Account, related_name="depositor", on_delete=models.CASCADE, null=True, blank=True)
  to_account = models.ForeignKey(Account, related_name="beneficiary", on_delete=models.CASCADE, null=True, blank=True)
  transaction_source = models.IntegerField(default=ATM, choices=TRANSACTION_SOURCE_CHOICES)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'transactions'
    verbose_name = 'Transaction'
    verbose_name_plural = 'Transactions'

    def __str__(self):
      return f'{self.account.id} - {self.amount}'