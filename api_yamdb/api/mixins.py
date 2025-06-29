from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAuthorModeratorAdminOrReadOnly, IsAdminOrReadOnly
from users.validators import username_validator


class RetrieveUpdateStatusHTTP405Mixin:
    """Миксин для возврата статуса 405 при попытке retrieve/update."""

    def retrieve(self, request, *args, **kwargs):
        """Возвращает статус 405 для GET запросов
        к детальному представлению."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        """Возвращает статус 405 для PUT/PATCH запросов."""
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class HTTPMethodNamesMixin:
    """Миксин для ограничения доступных HTTP-методов."""

    http_method_names = ('get', 'post', 'patch', 'delete')


class PermissionReviewCommentMixin:
    """Миксин с настройками прав доступа для отзывов и комментариев."""

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadOnly,
    )


class AdminSearchSlugMixin:
    """
    Миксин для:
    - Доступа только для админов (остальные - read-only)
    - Поиска по name
    - Использования slug как lookup-поля
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UsernameValidationMixin:
    '''Миксин для валидации логина пользователя.
    Проверяет:
    1. Что логин не равен 'me'.
    2. Что в логине не используются недопустимые символы.
    '''
    def validate_username(self, username):
        return username_validator(username)