import django_filters
from reviews.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    """Набор фильтров для модели Title."""

    # Поле фильтрации по жанру с использованием slug
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all()
    )

    # Поле фильтрации по категории с использованием slug
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year')
