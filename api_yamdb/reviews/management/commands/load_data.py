import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **options):
        # Загрузка пользователей
        with open('static/data/users.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )

        # Загрузка категорий
        with open('static/data/category.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )

        # Загрузка жанров
        with open('static/data/genre.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )

        # Загрузка произведений
        with open('static/data/titles.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )

        # Загрузка связей жанров и произведений
        with open('static/data/genre_title.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)

        # Загрузка отзывов
        with open('static/data/review.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )

        # Загрузка комментариев
        with open('static/data/comments.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )
