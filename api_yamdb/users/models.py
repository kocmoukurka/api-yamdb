from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (
    CONFIRMATION_CODE_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_FIRSTNAME_LENGTH,
    MAX_LASTNAME_LENGTH,
    MAX_USERNAME_LENGTH,
    ROLE_ADMIN,
    ROLE_MODERATOR,
    ROLE_USER,
)
from users.validators import username_validator


class RoleChoices(models.TextChoices):
    """Перечисление ролей пользователей для поля 'role' модели User."""

    USER = ROLE_USER, 'Аутентифицированный пользователь'
    MODERATOR = ROLE_MODERATOR, 'Модератор'
    ADMIN = ROLE_ADMIN, 'Администратор'


class User(AbstractUser):
    """Кастомная модель пользователя с расширенными полями."""

    username = models.CharField(
        verbose_name='Логин',
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        help_text=(
            'Обязательное поле. Не больше 150 символов. '
            'Только буквы, цифры и символы @/./+/-/_'
        ),
        validators=(username_validator,),
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        help_text='Обязательное поле.',
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_FIRSTNAME_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LASTNAME_LENGTH,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max(len(value) for value, _ in RoleChoices.choices),
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.is_superuser or self.role == RoleChoices.ADMIN

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == RoleChoices.MODERATOR
