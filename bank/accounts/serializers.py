from rest_framework import serializers

from bank.accounts.models import Account

class AccountSerializer(serializers.ModelSerializer):

  class Meta:
    model = Account
    fields = '__all__'