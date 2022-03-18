from django.test import TestCase
from bank.accounts.models import Account

from bank.factories.user import UserFactory
from bank.factories.account import AccountFactory

# Create your tests here.
class AccountTestCase(TestCase):
  def setUp(self):
    self.user = UserFactory()
    self.savings_account = AccountFactory(
      user=self.user,
      balance=1000,
      account_type=Account.SAVINGS
    )

    self.credit_account = AccountFactory(
      user=self.user,
      balance=10000,
      account_type=Account.CREDIT
    )

  def test_create_savings_account(self):
    assert(self.savings_account.user == self.user)
    assert(self.savings_account.balance == 1000)
    assert(self.savings_account.account_type == Account.SAVINGS)

  def test_create_credit_account(self):
    assert(self.credit_account.user == self.user)
    assert(self.credit_account.balance == 10000)
    assert(self.credit_account.account_type == Account.CREDIT)

  def test_update_account(self):
    self.savings_account.balance = 100
    self.savings_account.save()

    assert(self.savings_account.balance == 100)