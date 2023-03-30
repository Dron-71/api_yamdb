from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from .serializers import SignUpSerializer, TokenGenerationSerializer
from .tokens import JWTToken
from .utils import send_confirmation_code


User = get_user_model()


class SignUpView(APIView):
    """Sign up a new user."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if User.objects.filter(**serializer.data).exists():
            user = User.objects.get(**serializer.data)
            send_confirmation_code(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenGenerationView(APIView):
    """Generate JWT token."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenGenerationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=request.data.get('username'))
            user.is_active = True
            user.save()
            token = JWTToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
