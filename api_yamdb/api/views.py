"""
Модуль с основными view функциями и классами ViewSets для API сервиса YaMDB.
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import TitleFilter
from api.mixins import (
    AdminSearchSlugMixin,
    HTTPMethodNamesMixin,
    PermissionReviewCommentMixin,
    RetrieveUpdateStatusHTTP405Mixin,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class AdminSlugSearchViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый ViewSet для моделей с:
    - slug-идентификацией
    - поиском по name
    - ограниченными методами (GET-list, POST, DELETE)
    - админ-контролем доступа
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """ Обрабатывает запрос на регистрацию нового пользователя."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Генерирует JWT токен для пользователя после подтверждения кода."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.save(), status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def me(self, request):
        """Получение данных текущего пользователя."""
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

    @me.mapping.patch
    def update_me(self, request):
        """Обновление данных текущего пользователя."""
        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class CategoryViewSet(AdminSlugSearchViewSet):

    """ViewSet для работы с категориями произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class GenreViewSet(AdminSlugSearchViewSet):
    """ViewSet для работы с жанрами произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с произведениями (фильмы, книги и др.)."""

    queryset = Title.objects.annotate(
        avg_rating=Avg('reviews__score')
    ).order_by('-year')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter
    )
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    ordering_fields = ('name', 'year',)
    ordering = ('-year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class BaseReviewCommentViewSet(viewsets.ModelViewSet):
    """Базовый ViewSet для отзывов и комментариев."""
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadOnly
    )
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))


class ReviewViewSet(BaseReviewCommentViewSet):
    """ViewSet для работы с отзывами на произведения."""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(BaseReviewCommentViewSet):
    """ViewSet для работы с комментариями к отзывам."""

    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(
            self.get_title().reviews.all(),
            id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
