from django.test import TestCase

from bank.factories.user import UserFactory

# Create your tests here.
class AuthTestCase(TestCase):
  
  def setUp(self):
    user = UserFactory()
    print('SETUP', user)

  def test_login_user(self):
    print('CREATE AUTH')