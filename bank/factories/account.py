import factory

from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from bank.accounts.models import Account
from bank.factories.user import UserFactory

class AccountFactory(factory.django.DjangoModelFactory):

  class Meta:
    model = Account

  user = factory.SubFactory(UserFactory)
  account_type = Account.SAVINGS
  created_at = timezone.now()
  updated_at = timezone.now()