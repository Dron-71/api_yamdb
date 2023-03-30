from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from .permissions import IsAdmin
from .serializers import (SignUpSerializer, TokenGenerationSerializer,
                          UserMeSerializer, UserSerializer)
from .tokens import JWTToken
from .utils import send_confirmation_code


HTTP_METHOD_NAMES = [
    'get',
    'post',
    'patch',
    'delete',
    'head',
    'options',
    'trace',
]

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
            token = JWTToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Operations with users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = HTTP_METHOD_NAMES

    def get_serializer_class(self):
        if self.action == 'me':
            return UserMeSerializer
        return self.serializer_class

    def get_instance(self):
        return self.request.user

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        if request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
