from django.core.validators import RegexValidator


class UnicodeUsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = 'Enter a valid username.'
    flags = 0
