from django.conf import settings
from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bank.accounts.models import Account
from bank.transactions.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

  def create(self, validated_data):
    amount = validated_data.get('amount')
    user = validated_data.get('user', None)
    to_account = validated_data.get('to_account')
    reference = validated_data.get('reference', None)
    from_account = validated_data.get('from_account', None)
    transaction_type = validated_data.get('transaction_type')
    transaction_source = validated_data.get('transaction_source')

    if amount == 0:
      raise ValidationError('Amount must be greater 0')

    if transaction_type == Transaction.WITHDRAWAL:
      with transaction.atomic():
        if not from_account:
          raise ValidationError('Please specify "from_account" for this transaction.')
        
        new_balance = from_account.balance-amount

        if transaction_source == Transaction.EFT:
          raise ValidationError('You cannot withdraw using EFT.')

        if from_account.account_type == Account.SAVINGS \
            and new_balance < settings.SAVINGS_MINIMUM_BALANCE:
          raise ValidationError('You do not have enough funds to complete this transaction.')

        if from_account.account_type == Account.CREDIT \
            and new_balance < settings.CREDIT_MINIMUM_BALANCE:
          raise ValidationError('You do not have enough funds to complete this transaction.')

        
        txn = Transaction.objects.create(
          amount=amount,
          user=user,
          reference=reference,
          transaction_source=transaction_source,
          transaction_type=transaction_type,
          to_account=to_account,
          from_account=from_account,
          old_balance=from_account.balance,
          new_balance=new_balance
        )

        # Update Account balance
        from_account.balance = new_balance
        from_account.save()

        return txn

    if transaction_type == Transaction.DEPOSIT:
      with transaction.atomic():
        if not to_account:
          raise ValidationError('Please specify "to_account" for this transaction.')

        if transaction_source == Transaction.EFT:
          if not user:
            raise ValidationError('Only logged in user can do EFT Transaction.')
        
          if not from_account:
            raise ValidationError('"from_account" cannot not be empty for an ETF transaction.')
            
          if from_account.account_type == Account.SAVINGS \
              and from_account.balance < settings.SAVINGS_MINIMUM_BALANCE:
            raise ValidationError('You do not have enough funds to complete this transaction.')

          if from_account.account_type == Account.CREDIT \
              and from_account.balance < settings.CREDIT_MINIMUM_BALANCE:
            raise ValidationError('You do not have enough funds to complete this transaction.')


          from_account.balance -= amount
          from_account.save()

        # Create a new transaction
        new_balance = to_account.balance+amount
        
        txn = Transaction.objects.create(
          amount=amount,
          user=user,
          reference=reference,
          transaction_source=transaction_source,
          transaction_type=transaction_type,
          to_account=to_account,
          from_account=from_account,
          old_balance=to_account.balance,
          new_balance=new_balance
        )

        # Update Account balance
        to_account.balance = new_balance
        to_account.save()

        return txn



  class Meta:
    model = Transaction
    fields = '__all__'