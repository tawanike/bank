from django.test import TestCase
from django.urls import reverse

from bank.transactions.models import Transaction

from bank.factories.user import UserFactory
from bank.factories.account import AccountFactory
from bank.factories.transaction import TransactionFactory

class UserProfileTestCase(TestCase):

  def setUp(self):
    self.first_name = 'John'
    self.last_name = 'Doe'
    self.email = 'test@example.com'
    self.password = 'password'
    self.user = UserFactory(
      first_name=self.first_name, 
      last_name=self.last_name, 
      email=self.email, 
      password=self.password
    )

    self.account = AccountFactory(user=self.user)
    self.transaction_one = TransactionFactory(to_account=self.account, amount=100)
    self.transaction_two = TransactionFactory(to_account=self.account, amount=500)
    self.transaction_two = TransactionFactory(
      from_account=self.account, amount=500, 
      transaction_type=Transaction.WITHDRAWAL
    )

  def test_create_user(self):
    self.assertEqual(self.user.first_name, self.first_name)

  def test_admin_user_account_view(self):
    print(self.user.id)
    response = self.client.get(reverse('admin-user-view'), kwargs={'id': self.user.id})
    print(response)

