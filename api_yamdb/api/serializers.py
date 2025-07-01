from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from api.mixins import UsernameValidationMixin
from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(UserSerializer):
    """Сериализатор для эндпоинта users/me/."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer, UsernameValidationMixin):
    """Сериализатор для регистрации пользователей."""

    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGTH
    )
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH,
    )

    def validate(self, data):
        """Проверяет уникальность связки username и email."""
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(username=username).first()

        if user:
            if user.email != email:
                raise serializers.ValidationError(
                    'Пользователь с таким username уже зарегистрирован.'
                )
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован.'
            )
        return data

    def create(self, validated_data):
        """
        Создаёт пользователя, генерирует confirmation_code и отправляет email.
        """
        email = validated_data['email']
        username = validated_data['username']
        user, _ = User.objects.get_or_create(
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
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        """Проверяет корректность confirmation_code для указанного username."""
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError({
                'confirmation_code': 'Неверный код подтверждения.'
            })
        self.user = user
        return data

    def save(self, **kwargs):
        """Генерирует JWT-токен для пользователя."""
        token = AccessToken.for_user(self.user)
        return {'token': str(token)}


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        default=None,
        read_only=True,
        help_text="Средний рейтинг произведения"
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления произведений."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    # Добавлена проверка принадлежности хотя бы к одному жанру
    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError(
                'Произведение должно принадлежать хотя бы к одному жанру'
            )
        return value

    def to_representation(self, instance):
        return TitleReadSerializer(instance, context=self.context).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов на произведения."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        read_only_fields = ('title',)

    def validate(self, data):
        """
        Проверяет, что пользователь не оставлял отзыв на это произведение.
        """
        request = self.context.get('request')

        if request and request.method == 'POST':
            if Review.objects.filter(
                title=self.context.get('view').get_title().id,
                author=request.user
            ).exists():
                raise serializers.ValidationError({
                    'detail': 'Вы уже оставляли отзыв на это произведение.'
                })

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к отзывам."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
