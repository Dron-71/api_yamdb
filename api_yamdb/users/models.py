import os

from dotenv import load_dotenv

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import UsernameValidator


load_dotenv()


DEFAULT_USER_PASSWORD = os.getenv(
    'DEFAULT_USER_PASSWORD',
    default='some-password',
)


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    ]

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and '
            '@/./+/-/_ only. Not equal to "me".',
        ),
        validators=[UnicodeUsernameValidator(), UsernameValidator()],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(_('email_address'), max_length=254, unique=True)
    bio = models.TextField(_('biography'), blank=True)
    role = models.CharField(
        _('role'), max_length=9, choices=ROLE_CHOICES, default='user',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
