from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from .hashers import UserIdHasher


User = get_user_model()


def send_confirmation_code(user: User) -> None:
    """Send confirmation code by email."""
    confirmation_code = UserIdHasher().encode(user.pk)
    send_mail(
        subject=_('Ваш код подтверждения'),
        message=_(
            f'Пожалуйста, используйте <{confirmation_code}> как ваш код '
            ' подтверждения для активации аккаунта и получения JWT-токена.',
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
