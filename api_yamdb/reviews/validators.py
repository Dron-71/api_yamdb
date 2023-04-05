from datetime import datetime as dt

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(year_value: int) -> None:
    """Production year is not greater than current year."""
    current_year = dt.now().year
    if year_value > current_year:
        raise ValidationError(
            _('Год выпуска не должен быть больше текущего!'),
        )
