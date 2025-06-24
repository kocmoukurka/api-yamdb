from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Получаем базовую модель User


class NamedDescriptionAbstract(models.Model):
    """
    Абстрактный класс для наследования с общим полем name.
    Подходит для любых моделей, где необходимо уникальное наименование.
    """
    # Название объекта
    name = models.CharField(verbose_name='Название',
                            max_length=256)

    class Meta:
        abstract = True  # Класс объявлен абстрактным


class CategoryGenreAbstract(NamedDescriptionAbstract):
    """
    Абстрактный класс для наследования моделями Category и Genre.
    Содержит дополнительное поле slug для уникального адреса ресурса.
    """
    # Уникальное адресное поле для ссылок
    slug = models.SlugField(verbose_name='Слаг', max_length=50,
                            unique=True)

    class Meta:
        abstract = True  # Класс объявлен абстрактным


class Category(CategoryGenreAbstract):
    """
    Модель категории произведений.
    Описывает типы категорий, к которым относятся произведения.
    """
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        # Возвращает короткое строковое представление объекта
        return self.name[:20]


class Genre(CategoryGenreAbstract):
    """
    Модель жанра произведений. Представляет собой набор возможных жанров,
    к которым принадлежат произведения.
    """
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        # Возвращает короткое строковое представление объекта
        return self.name[:20]


class Title(NamedDescriptionAbstract):
    """
    Основная модель произведения.
    Включает базовые характеристики произведения, такие как год выпуска,
    категория, жанр, рейтинг и прочее.
    """
    # Год выпуска произведения
    year = models.IntegerField(
        verbose_name='Год выхода')
    # Произведение может относиться к нескольким жанрам
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    # Внешний ключ на категорию
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория')
    # Рейтинг произведения
    rating = models.IntegerField(
        verbose_name='Рейтинг', null=True, blank=True)
    # Подробное описание произведения
    description = models.TextField(verbose_name='Описание')
    # Изображение обложки
    image = models.ImageField(upload_to='titles/', null=True,
                              blank=True,
                              verbose_name='Изображение')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        # Имя для обратных связей по умолчанию
        default_related_name = 'titles'
        # Порядок сортировки по убыванию года выпуска
        ordering = ('-year', )

    def __str__(self):
        # Возвращает короткое строковое представление объекта
        return self.name[:20]
