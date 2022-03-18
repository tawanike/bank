import factory

from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserFactory(factory.django.DjangoModelFactory):

  class Meta:
    model = User
    django_get_or_create = ('username',)

  first_name = factory.Faker('first_name')
  last_name = factory.Faker('last_name')
  email = factory.Faker('email')
  password = make_password('password')
  date_joined = timezone.now()
  username = factory.Faker('email')
  is_superuser = False
  is_staff = False
  is_active = True