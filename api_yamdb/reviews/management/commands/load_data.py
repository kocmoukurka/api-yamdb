import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **options):
        data_to_load = {
            User: {
                'file': f'{settings.BASE_DIR}/static/data/users.csv',
                'fields': {
                    'id': 'id',
                    'username': 'username',
                    'email': 'email',
                    'role': 'role',
                    'bio': 'bio',
                    'first_name': 'first_name',
                    'last_name': 'last_name'
                },
                'relations': {}
            },
            Category: {
                'file': f'{settings.BASE_DIR}/static/data/category.csv',
                'fields': {
                    'id': 'id',
                    'name': 'name',
                    'slug': 'slug'
                },
                'relations': {}
            },
            Genre: {
                'file': f'{settings.BASE_DIR}/static/data/genre.csv',
                'fields': {
                    'id': 'id',
                    'name': 'name',
                    'slug': 'slug'
                },
                'relations': {}
            },
            Title: {
                'file': f'{settings.BASE_DIR}/static/data/titles.csv',
                'fields': {
                    'id': 'id',
                    'name': 'name',
                    'year': 'year',
                    'category_id': 'category'
                },
                'relations': {}
            },
            Review: {
                'file': f'{settings.BASE_DIR}/static/data/review.csv',
                'fields': {
                    'id': 'id',
                    'title_id': 'title_id',
                    'text': 'text',
                    'author_id': 'author',
                    'score': 'score',
                    'pub_date': 'pub_date'
                },
                'relations': {}
            },
            Comment: {
                'file': f'{settings.BASE_DIR}/static/data/comments.csv',
                'fields': {
                    'id': 'id',
                    'review_id': 'review_id',
                    'text': 'text',
                    'author_id': 'author',
                    'pub_date': 'pub_date'
                },
                'relations': {}
            }
        }

        # Загрузка основных данных
        for model, config in data_to_load.items():
            objects_to_create = []
            with open(config['file'], encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    fields = {}
                    for field, column in config['fields'].items():
                        fields[field] = row[column]
                    objects_to_create.append(model(**fields))

            if objects_to_create:
                model.objects.bulk_create(objects_to_create)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Успешно загружено {len(objects_to_create)} {model.__name__} записей'
                    )
                )

        # Загрузка связей между жанрами и произведениями
        genre_title_objects = []
        with open(f'{settings.BASE_DIR}/static/data/genre_title.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
                genre_title_objects.append((title.id, genre.id))

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно загружено {len(genre_title_objects)} genre-title связей'
            )
        )
