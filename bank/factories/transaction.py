import factory

from bank.transactions.models import Transaction

from bank.factories.user import UserFactory
from bank.factories.account import AccountFactory

class TransactionFactory(factory.django.DjangoModelFactory):

  class Meta:
    model = Transaction

  user = factory.SubFactory(UserFactory)
  reference = 'Transaction reference'
  from_account = factory.SubFactory(AccountFactory)
  to_account = factory.SubFactory(AccountFactory)
