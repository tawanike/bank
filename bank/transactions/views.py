from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.schemas.openapi import AutoSchema

from bank.transactions.models import Transaction
from bank.transactions.serializers import TransactionSerializer


class TransactionsAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all() # Change to filter by loggedin user

class TransactionAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_field = 'id'
