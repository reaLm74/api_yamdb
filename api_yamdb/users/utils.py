from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def send_confirmation_code(user):
    """Отправление кода на почту."""
    return send_mail(
        'Код подтверждения',
        f'{default_token_generator.make_token(user)} - код',
        DEFAULT_FROM_EMAIL,
        [user.email]
    )
