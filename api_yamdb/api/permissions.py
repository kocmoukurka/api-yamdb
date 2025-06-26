from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ('GET', 'HEAD', 'OPTIONS')
            or (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))
        )


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET', 'HEAD', 'OPTIONS')
            or request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user
        )
