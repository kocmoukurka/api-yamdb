from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (
    CONFIRMATION_CODE_LENGTH, MAX_EMAIL_LENGHT, MAX_FIRSTNAME_LENGTH,
    MAX_LASTNAME_LENGTH, MAX_ROLE_LENGTH, MAX_USERNAME_LENGHT, ROLE_ADMIN,
    ROLE_MODERATOR, ROLE_USER
)
from .validators import username_validator


ROLES = (
    (ROLE_USER, 'Аутентифицированный пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
)


class CustomUser(AbstractUser):
    '''Кастомная модель пользователя.'''
    username = models.CharField(
        verbose_name='Логин',
        max_length=MAX_USERNAME_LENGHT,
        unique=True,
        help_text='Обязательное поле. Не больше 150 символов. Только буквы,'
        'цифры и символы @/./+/-/_',
        validators=(username_validator,)
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=MAX_EMAIL_LENGHT,
        unique=True,
        help_text='Обязательное поле.'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_FIRSTNAME_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LASTNAME_LENGTH,
        blank=True
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_ROLE_LENGTH,
        choices=ROLES,
        default=ROLE_USER,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username