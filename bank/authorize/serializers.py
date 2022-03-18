from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class AuthSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('Email is required.')

        if password is None:
            raise serializers.ValidationError('Password is required.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('Email/Password provided is not valid.')

        if not user.is_active:
            raise serializers.ValidationError({'code': 403, 'message': 'Account is not activated.', 'user': user.id })

        refresh = RefreshToken.for_user(user)

        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return token
