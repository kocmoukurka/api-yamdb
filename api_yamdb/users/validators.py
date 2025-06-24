from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


regex_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Разрешены только буквы, цифры и символы @/./+/-/_',
    code='invalid_username'
)


def username_validator(username):
    if username == 'me':
        raise ValidationError(
            f'Логин "{username}" запрещён.'
        )
    regex_validator(username)
