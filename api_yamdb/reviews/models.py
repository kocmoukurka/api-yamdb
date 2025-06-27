"""Модели для приложения reviews."""

from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import (
    MAX_LINE_LENGTH,
    MAX_NAME_LENGTH,
    MAX_SLUG_LENGHT,
)

User = get_user_model()


class NamedAbstract(models.Model):
    """Абстрактная модель с полем name.
    Подходит для любых моделей, где необходимо уникальное наименование.
    """

    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_NAME_LENGTH
    )

    class Meta:
        abstract = True


class CategoryGenreAbstract(NamedAbstract):
    """Абстрактная модель для категорий и жанров.
    Содержит дополнительное поле slug для уникального адреса ресурса.
    """

    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_SLUG_LENGHT,
        unique=True
    )

    class Meta:
        abstract = True


class UserTextPubDateAbstract(models.Model):
    """Абстрактная модель для отзывов и комментариев.
    Содержит общую информацию о создателе текста:
    - автор
    - текст
    - дата создания
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Category(CategoryGenreAbstract):
    """Модель категории произведений."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LINE_LENGTH]


class Genre(CategoryGenreAbstract):
    """Модель жанра произведений."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_LINE_LENGTH]


class Title(NamedAbstract):
    """Модель произведения (фильмы, книги и др.)."""

    year = models.IntegerField(verbose_name='Год выхода')
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('-year',)

    def __str__(self):
        return self.name[:MAX_LINE_LENGTH]


class Review(UserTextPubDateAbstract):
    """Модель отзыва на произведение."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.IntegerField(verbose_name='Оценка отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review_per_author'
            )
        ]
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:MAX_LINE_LENGTH]


class Comment(UserTextPubDateAbstract):
    """Модель комментария к отзыву."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:MAX_LINE_LENGTH]
