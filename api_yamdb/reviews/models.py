# reviews/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth import get_user_model

User = get_user_model()  # Получаем базовую модель User



class NamedAbstract(models.Model):

    """
    Абстрактный класс для наследования с общим полем name.
    Подходит для любых моделей, где необходимо уникальное наименование.
    """
    # Название объекта

    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )

    class Meta:
        abstract = True  # Класс объявлен абстрактным


class CategoryGenreAbstract(NamedAbstract):

    """
    Абстрактный класс для наследования моделями Category и Genre.
    Содержит дополнительное поле slug для уникального адреса ресурса.
    """
    # Уникальное адресное поле для ссылок

    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True  # Класс объявлен абстрактным


class UserTextPubDateAbstract(models.Model):
    """
    Абстрактный класс для моделей отзывов и комментариев.
    Содержит общую информацию о создателе текста (автор, текст, дата создания).
    """
    # Автор публикации
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    # Основной текст публикации
    text = models.TextField()
    # Дата создания поста или комментария
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True  # Класс объявлен абстрактным


class Category(CategoryGenreAbstract):
    """
    Модель категории произведений.
    Описывает типы категорий, к которым относятся произведения.
    """
    class Meta:
        # Человеческое представление единичной категории
        verbose_name = 'Категория'
        # Человеческое представление множественного числа
        verbose_name_plural = 'Категории'

    def __str__(self):
        # Возвращает короткое строковое представление объекта
        return self.name[:20]


class Genre(CategoryGenreAbstract):
    """
    Модель жанра произведений.
    Представляет собой набор возможных жанров, к которым принадлежат
    произведения.

    """
    class Meta:
        # Человеческое представление единичного жанра
        verbose_name = 'Жанр'
        # Человеческое представление множественного числа
        verbose_name_plural = 'Жанры'

    def __str__(self):
        # Возвращает короткое строковое представление объекта
        return self.name[:20]



class Title(NamedAbstract):

    """
    Основная модель произведения.
    Включает базовые характеристики произведения, такие как год выпуска,
    категория, жанр, рейтинг и прочее.
    """
    # Год выпуска произведения
    year = models.IntegerField(
        verbose_name='Год выхода'
    )
    # Произведение может относиться к нескольким жанрам
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    # Внешний ключ на категорию
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        null=True,
        blank=True
    )
    # Рейтинг произведения (может быть пустым)
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        blank=True
    )
    # Подробное описание произведения
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    # Изображение обложки (опционально)
    image = models.ImageField(
        upload_to='titles/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )

    class Meta:
        # Человеческое представление единичного произведения
        verbose_name = 'Произведение'
        # Человеческое представление множественного числа
        verbose_name_plural = 'Произведения'
        # Имя для обратных связей по умолчанию
        default_related_name = 'titles'
        # Порядок сортировки по убыванию года выпуска

        ordering = (
            '-year',
        )


    def __str__(self):
        # Возвращает короткое строковое представление объекта
        return self.name[:20]


class Review(UserTextPubDateAbstract):
    """
    Модель отзыва.
    Связана с произведением и включает оценку и текст отзыва.
    """
    # Пост, которому принадлежит отзыв
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Пост'
    )
    # Оценка отзыва (числовое значение)
    score = models.IntegerField(
        verbose_name='Оценка отзыва'
    )

    class Meta:
        # Человеческое представление единичного отзыва
        verbose_name = 'Отзыв'
        # Человеческое представление множественного числа
        verbose_name_plural = 'Отзывы'
        # Имя для обратных связей по умолчанию
        default_related_name = 'reviews'
        # Порядок сортировки по убыванию даты создания
        ordering = (
            '-pub_date',
        )

    def __str__(self):
        # Возвращает короткий отрывок текста отзыва
        return self.text[:20]


class Comment(UserTextPubDateAbstract):
    """
    Модель комментария.
    Связана с отзывом и включает текст комментария.
    """
    # Отзыв, к которому относится комментарий
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        # Человеческое представление единичного комментария
        verbose_name = 'Комментарий'
        # Человеческое представление множественного числа
        verbose_name_plural = 'Комментарии'
        # Имя для обратных связей по умолчанию
        default_related_name = 'comments'
        # Порядок сортировки по убыванию даты создания
        ordering = (
            '-pub_date',
        )

    def __str__(self):
        # Возвращает короткий отрывок текста комментария
        return self.text[:20]

