from users.validators import username_validator


class UsernameValidationMixin:
    '''Миксин для валидации логина пользователя.
    Проверяет:
    1. Что логин не равен 'me'.
    2. Что в логине не используются недопустимые символы.
    '''
    def validate_username(self, username):
        return username_validator(username)