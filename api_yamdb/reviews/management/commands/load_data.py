import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Загрузка данных из csv-файлов'

    def handle(self, *args, **options):
        load_data_dir = f'{settings.BASE_DIR}/static/data/'
        category_genre_fields = {
            'id': 'id',
            'name': 'name',
            'slug': 'slug'
        }
        id_text_author_pub_date_fields = {
            'id': 'id',
            'text': 'text',
            'author_id': 'author',
            'pub_date': 'pub_date'
        }
        data_to_load = {
            User: {
                'file': f'{load_data_dir}users.csv',
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
                'file': f'{load_data_dir}category.csv',
                'fields': category_genre_fields,
                'relations': {}
            },
            Genre: {
                'file': f'{load_data_dir}genre.csv',
                'fields': category_genre_fields,
                'relations': {}
            },
            Title: {
                'file': f'{load_data_dir}titles.csv',
                'fields': {
                    'id': 'id',
                    'name': 'name',
                    'year': 'year',
                    'category_id': 'category'
                },
                'relations': {}
            },
            Review: {
                'file': f'{load_data_dir}review.csv',
                'fields': id_text_author_pub_date_fields | {
                    'title_id': 'title_id',
                    'score': 'score',
                },
                'relations': {}
            },
            Comment: {
                'file': f'{load_data_dir}comments.csv',
                'fields': id_text_author_pub_date_fields | {
                    'review_id': 'review_id',
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
                        (
                            f'Успешно загружено {len(objects_to_create)}'
                            f' {model.__name__} записей'
                        )
                    )
                )

            # Загрузка связей между жанрами и произведениями
        genre_title_objects = []
        with open(f'{load_data_dir}genre_title.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
                genre_title_objects.append((title.id, genre.id))

        self.stdout.write(
            self.style.SUCCESS(
                (
                    f'Успешно загружено {len(genre_title_objects)}'
                    ' genre-title связей'
                )
            )
        )
