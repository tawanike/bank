from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from bank.accounts.models import Account
from bank.transactions.models import Transaction

from bank.factories.user import UserFactory
from bank.factories.account import AccountFactory

# Create your tests here.
class TransactionTestCase(TestCase):
  def setUp(self):
    self.savings_account = AccountFactory(
      account_type=Account.SAVINGS,
      balance=50.00
    )
    self.credit_account = AccountFactory(
      account_type=Account.CREDIT
    )

  def test_create_eft_deposit_transaction(self):
    txn = dict(
      to_account =self.savings_account.id,
      from_account = self.credit_account.id,
      amount=100.00,
      transaction_type=Transaction.DEPOSIT,
      transaction_source=Transaction.EFT,
      user=UserFactory().id
    )

    response = self.client.post(reverse('transactions'), txn)
    data = response.json()
    self.assertEqual(response.status_code, 201)
    # TODO tawanda ensure that the balance from accounts always has 2 decimal places
    self.assertEqual(data.get('old_balance'), f'{self.savings_account.balance:.2f}')
    new_balance = txn.get('amount')+self.savings_account.balance
    self.assertEqual(data.get('new_balance'), f'{new_balance:.2f}')
    self.assertEqual(data.get('amount'), f'{txn.get("amount"):.2f}')
    self.assertEqual(data.get('transaction_source'), Transaction.EFT)
    self.assertEqual(data.get('transaction_type'), Transaction.DEPOSIT)
    self.assertEqual(data.get('to_account'), self.savings_account.id)
    self.assertEqual(data.get('from_account'), self.credit_account.id)
    

  def test_create_eft_withdrawal_transaction(self):
    txn = dict(
      to_account =self.savings_account.id,
      from_account = self.credit_account.id,
      amount=100.00,
      transaction_type=Transaction.WITHDRAWAL,
      transaction_source=Transaction.EFT,
      user=UserFactory().id
    )

    response = self.client.post(reverse('transactions'), txn)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json()[0], 'You cannot withdraw using EFT.')


  def test_create_atm_deposit_transaction(self):
    txn = dict(
      to_account =self.savings_account.id,
      amount=100.00,
      transaction_type=Transaction.DEPOSIT,
      transaction_source=Transaction.ATM
    )

    response = self.client.post(reverse('transactions'), txn)
    data = response.json()
    self.assertEqual(response.status_code, 201)
    # TODO tawanda ensure that the balance from accounts always has 2 decimal places
    self.assertEqual(data.get('old_balance'), f'{self.savings_account.balance:.2f}')
    new_balance = txn.get('amount')+self.savings_account.balance
    self.assertEqual(data.get('new_balance'), f'{new_balance:.2f}')
    self.assertEqual(data.get('amount'), f'{txn.get("amount"):.2f}')
    self.assertEqual(data.get('transaction_source'), Transaction.ATM)
    self.assertEqual(data.get('transaction_type'), Transaction.DEPOSIT)
    self.assertEqual(data.get('to_account'), self.savings_account.id)

  def test_create_atm_withdrawal_transaction(self):
    savings_account = AccountFactory(balance=Decimal(150.00))

    txn = dict(
      from_account = savings_account.id,
      amount=Decimal(100.00),
      transaction_type=Transaction.WITHDRAWAL,
      transaction_source=Transaction.ATM
    )

    response = self.client.post(reverse('transactions'), txn)
    data = response.json()
    self.assertEqual(response.status_code, 201)

    # TODO tawanda ensure that the balance from accounts always has 2 decimal places
    self.assertEqual(data.get('old_balance'), f'{savings_account.balance:.2f}')
    
    new_balance = savings_account.balance - txn.get('amount')

    self.assertEqual(data.get('new_balance'), f'{new_balance:.2f}')
    self.assertEqual(data.get('amount'), f'{txn.get("amount"):.2f}')
    self.assertEqual(data.get('transaction_source'), Transaction.ATM)
    self.assertEqual(data.get('transaction_type'), Transaction.WITHDRAWAL)
    self.assertEqual(data.get('from_account'), savings_account.id)


  def test_create_bank_deposit_transaction(self):
    txn = dict(
      to_account =self.savings_account.id,
      amount=100.00,
      transaction_type=Transaction.DEPOSIT,
      transaction_source=Transaction.BRANCH
    )

    response = self.client.post(reverse('transactions'), txn)
    data = response.json()
    self.assertEqual(response.status_code, 201)
    # TODO tawanda ensure that the balance from accounts always has 2 decimal places
    self.assertEqual(data.get('old_balance'), f'{self.savings_account.balance:.2f}')
    new_balance = txn.get('amount')+self.savings_account.balance
    self.assertEqual(data.get('new_balance'), f'{new_balance:.2f}')
    self.assertEqual(data.get('amount'), f'{txn.get("amount"):.2f}')
    self.assertEqual(data.get('transaction_source'), Transaction.BRANCH)
    self.assertEqual(data.get('transaction_type'), Transaction.DEPOSIT)
    self.assertEqual(data.get('to_account'), self.savings_account.id)

  def test_create_bank_withdrawal_transaction(self):
    credit_account = AccountFactory(balance=Decimal(-150.00), account_type=Account.CREDIT)

    txn = dict(
      from_account = credit_account.id,
      amount=Decimal(100.00),
      transaction_type=Transaction.WITHDRAWAL,
      transaction_source=Transaction.ATM
    )

    response = self.client.post(reverse('transactions'), txn)
    data = response.json()
    self.assertEqual(response.status_code, 201)

    # TODO tawanda ensure that the balance from accounts always has 2 decimal places
    self.assertEqual(data.get('old_balance'), f'{credit_account.balance:.2f}')
    
    new_balance = credit_account.balance - txn.get('amount')

    self.assertEqual(data.get('new_balance'), f'{new_balance:.2f}')
    self.assertEqual(data.get('amount'), f'{txn.get("amount"):.2f}')
    self.assertEqual(data.get('transaction_source'), Transaction.ATM)
    self.assertEqual(data.get('transaction_type'), Transaction.WITHDRAWAL)
    self.assertEqual(data.get('from_account'), credit_account.id)

  def test_insufficient_funds_savings_transaction(self):
    credit_account = AccountFactory(balance=Decimal(100.00), account_type=Account.SAVINGS)

    txn = dict(
      from_account = credit_account.id,
      amount=Decimal(100.00),
      transaction_type=Transaction.WITHDRAWAL,
      transaction_source=Transaction.ATM
    )

    response = self.client.post(reverse('transactions'), txn)
    data = response.json()
    self.assertEqual(response.status_code, 400)
    self.assertEqual(data[0], 'You do not have enough funds to complete this transaction.')


  def test_insufficient_funds_credit_transaction(self):
    credit_account = AccountFactory(balance=Decimal(-100.00), account_type=Account.SAVINGS)

    txn = dict(
      from_account = credit_account.id,
      amount=Decimal(20000.00),
      transaction_type=Transaction.WITHDRAWAL,
      transaction_source=Transaction.ATM
    )

    response = self.client.post(reverse('transactions'), txn)
    data = response.json()
    self.assertEqual(response.status_code, 400)
    self.assertEqual(data[0], 'You do not have enough funds to complete this transaction.')