from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.contrib.auth.models import User
from bank.users.serializers import UserSerializer


class UsersAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer
    queryset = User.objects.all() # Change to filter by loggedin user


class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class UserAdminAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'