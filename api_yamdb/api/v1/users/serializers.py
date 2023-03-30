from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .hashers import UserIdHasher
from .utils import send_confirmation_code


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer to sign up a new user."""

    class Meta:
        model = User
        fields = ('email', 'username')

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        obj = User.objects.create(
            username=username,
            email=email,
        )
        send_confirmation_code(user=obj)


class TokenGenerationSerializer(serializers.Serializer):
    """Serializer to token generation."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=64)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        check = UserIdHasher().check_code(data['confirmation_code'], user.pk)
        if not check:
            raise serializers.ValidationError(
                {'confirmation_code': 'Введен неверный код подтверждения.'},
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer to work with users (for admin only)."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(UserSerializer):
    """Serializer to work with current user."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
