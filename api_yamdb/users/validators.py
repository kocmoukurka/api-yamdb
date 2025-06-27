from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


regex_validator = RegexValidator(
    regex=r'^[\w.@+-]+$',
    message='Разрешены только буквы, цифры и символы @/./+/-/_',
    code='invalid_username'
)


def username_validator(username):
    """Валидатор для проверки имени пользователя.

    Проверяет:
    1. Что имя пользователя не равно 'me'
    2. Что имя соответствует regex-паттерну

    Args:
        username (str): Проверяемое имя пользователя

    Raises:
        ValidationError: Если имя не проходит валидацию
    """
    if username == 'me':
        raise ValidationError(
            f'Логин "{username}" запрещён.'
        )
    regex_validator(username)
