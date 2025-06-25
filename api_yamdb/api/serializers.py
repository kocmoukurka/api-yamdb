from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Review, Comment
from users.constants import MAX_EMAIL_LENGHT, MAX_USERNAME_LENGHT


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGHT
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        required=True,
        max_length=MAX_USERNAME_LENGHT,
    )

    def validate_username(self, value):
        '''Проверка username на запрет использования слова "me"
        в качестве логина.
        '''
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value

    def validate(self, data):
        '''Проверка связки username и email.
        Для пользователя с уже существующим логином:
            - если email отличается — ошибка.
            - если email совпадает — повторно отправляется код подтверждения.
        Если email уже используется другим пользователем — ошибка.
        '''
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


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )


class TitleWriteSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'  
        read_only_fields = ('title',)    

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне от 1 до 10.'
                )
        return value 


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
