"""
Модуль с основными view функциями и классами ViewSets для API сервиса YaMDB.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend


from api.mixins import (
    HTTPMethodNamesMixin,
    PermissionReviewCommentMixin,
    RetrieveUpdateStatusHTTP405,
)
from api.permissions import IsAdmin, IsAdminOrReadOnly
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
from api.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """ Обрабатывает запрос на регистрацию нового пользователя.
    Отправляет письмо с кодом подтверждения на указанный email.
    """
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    username = serializer.validated_data['username']

    user, created = User.objects.get_or_create(
        email=email,
        username=username
    )

    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()

    send_mail(
        subject='YaMDb confirmation code',
        message=f'Your confirmation code: {confirmation_code}',
        from_email='yamdb@example.com',
        recipient_list=[email],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Генерирует JWT токен для пользователя после подтверждения кода."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']

    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            {'confirmation_code': 'Invalid confirmation code'},
            status=status.HTTP_400_BAD_REQUEST
        )

    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(HTTPMethodNamesMixin, viewsets.ModelViewSet):
    """ViewSet для управления пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request):
        """Получение и обновление данных текущего пользователя."""
        if request.method == 'GET':
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data)

        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryViewSet(RetrieveUpdateStatusHTTP405, viewsets.ModelViewSet):
    """ViewSet для работы с категориями произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(RetrieveUpdateStatusHTTP405, viewsets.ModelViewSet):
    """ViewSet для работы с жанрами произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(HTTPMethodNamesMixin, viewsets.ModelViewSet):
    """ViewSet для работы с произведениями (фильмы, книги и др.)."""
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    # Обработка ошибок валидации
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReviewViewSet(
    HTTPMethodNamesMixin,
    PermissionReviewCommentMixin,
    viewsets.ModelViewSet
):
    """ViewSet для работы с отзывами на произведения."""

    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        if Review.objects.filter(
            title=title,
            author=self.request.user
        ).exists():
            raise ValidationError(
                {'detail': 'Вы уже оставляли отзыв на это произведение.'}
            )
        serializer.save(author=self.request.user, title=title)
        self.update_title_rating(title)

    def perform_destroy(self, instance):
        title = instance.title
        instance.delete()
        self.update_title_rating(title)

    def update_title_rating(self, title):
        from django.db.models import Avg
        result = title.reviews.aggregate(average=Avg('score'))
        title.rating = result['average'] or 0
        title.save(update_fields=['rating'])


class CommentViewSet(
    HTTPMethodNamesMixin,
    PermissionReviewCommentMixin,
    viewsets.ModelViewSet
):
    """ViewSet для работы с комментариями к отзывам."""

    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
