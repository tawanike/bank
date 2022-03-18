from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
  SAVINGS = 0
  CREDIT = 1

  ACCOUNT_TYPE_CHOICES = (
    (SAVINGS, 'Savings'),
    (CREDIT, 'Credit'),
  )

  user = models.ForeignKey(User, related_name="account", on_delete=models.CASCADE)
  account_type = models.IntegerField(default=SAVINGS, choices=ACCOUNT_TYPE_CHOICES)
  balance = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'accounts'
    verbose_name = 'Account'
    verbose_name_plural = 'Accounts'

    def __str__(self):
      return f'{self.user.first_name} - {self.id}'