from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class NamedDescriptionAbstract(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    description = models.TextField(verbose_name='Описание')

    class Meta:
        abstract = True


class CategoryGenreAbstract(NamedDescriptionAbstract):
    slug = models.SlugField(verbose_name='Слаг', unique=True)

    class Meta:
        abstract = True


class UserTextCreationAbstract(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    text = models.TextField()
    created = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class Category(CategoryGenreAbstract):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:20]


class Genre(CategoryGenreAbstract):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:20]


class Title(NamedDescriptionAbstract):
    year = models.IntegerField(
        verbose_name='Год выхода')
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг')
    image = models.ImageField(
        upload_to='titles/', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('-year',)

    def __str__(self):
        return self.name[:20]


class Review(UserTextCreationAbstract):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Пост'
    )
    score = models.IntegerField(
        verbose_name='Оценка отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:20]


class Comment(UserTextCreationAbstract):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:20]
