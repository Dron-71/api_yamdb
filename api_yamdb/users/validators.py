from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(RegexValidator):
    """Username not equal 'me'."""

    regex = r'^me$'
    inverse_match = True
    message = _('Username can not be equal to "me".')
    flags = 0
