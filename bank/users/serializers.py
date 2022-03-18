from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import User

from bank.accounts.models import Account
from bank.accounts.serializers import AccountSerializer
from bank.transactions.models import Transaction
from bank.transactions.serializers import TransactionSerializer

class UserSerializer(serializers.ModelSerializer):
  accounts = AccountSerializer(many=True, source="account")
  transactions = TransactionSerializer(many=True)

  def to_representation(self, instance):

    representation = super(UserSerializer, self).to_representation(instance)
    representation['transactions'] = TransactionSerializer(self.instance.transactions.all()[:10], many=True).data
    return representation

  def create(self, validated_data):
    email = validated_data.get('email')
    password = validated_data.get('password')

    try:
        user = User.objects.get(email=email)
        if user:
            key_error = "user_exists"
            raise ValidationError('Email address taken.', code=key_error)
    except User.DoesNotExist:
        user = User.objects.create(**validated_data)
        user.username = email
        user.set_password(password)
        user.save()

  class Meta:
    model = User
    fields = [
            'id', 'first_name', 'last_name', 'email', 'is_active', 'accounts', 'transactions'
        ]
    extra_kwargs = {'password': {'write_only': True}}
