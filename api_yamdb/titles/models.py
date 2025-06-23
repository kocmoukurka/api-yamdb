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
    image = models.ImageField(
        upload_to='titles/', null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('-year',)

    def __str__(self):
        return self.name[:20]
