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
        subject=_('Your confirmation code'),
        message=_(
            f'Please, use <{confirmation_code}> as your confirmation code '
            'to activate your account and get JWT-token.',
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
