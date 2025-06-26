from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAuthorModeratorAdminOrReadOnly


class RetrieveUpdateStatusHTTP405:
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
