from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from bank.accounts.models import Account
from bank.accounts.serializers import AccountSerializer


class AccountsAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AccountSerializer
    queryset = Account.objects.all() # Change to filter by loggedin user

class AccountAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = 'id'