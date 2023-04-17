from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_year(value):
    if value > now().year:
        raise ValidationError(
            'Введите корректный год',
            params={"value": value}
        )
