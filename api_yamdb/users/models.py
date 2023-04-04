from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import UsernameValidator


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
        _('Имя пользователя'),
        max_length=150,
        unique=True,
        help_text=_(
            'Обязательное поле. 150 символов или меньше. Только буквы, '
            'цифры и символы "@/./+/-/_". Не равно "me".'
        ),
        validators=[UnicodeUsernameValidator(), UsernameValidator()],
        error_messages={
            'unique': _('Пользователь с таким именем уже существует.'),
        },
    )
    email = models.EmailField(
        _('Электронная почта'),
        max_length=254,
        unique=True,
    )
    bio = models.TextField(_('О себе'), blank=True)
    role = models.CharField(
        _('Роль'), max_length=9, choices=ROLE_CHOICES, default='user',
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
