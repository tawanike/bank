from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from bank.authorize.serializers import AuthSerializer


class AuthAPIView(APIView):
    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_400_BAD_REQUEST)
