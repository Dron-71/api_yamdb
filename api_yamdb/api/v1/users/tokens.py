from datetime import timedelta

from rest_framework_simplejwt.tokens import AccessToken

from django.conf import settings


DEFAULT_TOKEN_LIFETIME: int = 30


class JWTToken(AccessToken):
    """
    JWT access token.

    Token lifetime is taken from the SIMPLE_JWT configuration in
    settings.py or the default value is used.
    """

    lifetime = settings.SIMPLE_JWT.get(
        'ACCESS_TOKEN_LIFETIME',
        timedelta(days=DEFAULT_TOKEN_LIFETIME),
    )
