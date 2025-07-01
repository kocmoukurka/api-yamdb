# YaMDb - API для отзывов на произведения

# О проекте
YaMDb собирает отзывы пользователей на произведения искусства (книги, фильмы, музыку). Это REST API сервис с системой рейтингов и комментариев, где:

Произведения делятся на категории ("Книги", "Фильмы", "Музыка")

Каждое произведение имеет жанры (например, "Сказка", "Рок")

Пользователи оставляют отзывы и ставят оценки (1-10)

Формируется средний рейтинг произведения

К отзывам можно добавлять комментарии

# Технологический стек
Backend: Python 3.9+, Django 5.1, Django REST Framework 3.15

Аутентификация: JWT (djangorestframework-simplejwt)

База данных: SQLite

Документация: Redoc

Дополнительно: Pillow (для изображений)

# Быстрый старт
Установка и настройка
bash
## Клонирование репозитория
git clone https://github.com/kocmoukurka/api_yamdb.git
cd api_yamdb

## Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate    # Windows

## Установка зависимостей
pip install -r requirements.txt

## Настройка базы данных
python manage.py migrate
python manage.py load_data # Опционально: тестовые данные

## Создание администратора
```
python manage.py createsuperuser
```

## Запуск сервера
```
python manage.py runserver
```
Документация API будет доступна по адресу:
http://127.0.0.1:8000/redoc/

# API Endpoints
## Аутентификация
POST /api/v1/auth/signup/ - Регистрация нового пользователя
```
{
"email": "user@example.com",
"username": "user"
}
```
Ответ 
```
{
"email": "string",
"username": "string"
}
```
POST /api/v1/auth/token/ - Получение JWT-токена
```
{
"username": "user",
"confirmation_code": "string"
}
```
Ответ
```
{
"token": "string"
}
```

## Контент
GET /api/v1/titles/ - Список произведений
Ответ
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```

POST /api/v1/titles/{title_id}/reviews/ - Добавление отзыва
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Ответ
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ],
  "category": {
    "name": "string",
    "slug": "^-$"
  }
}
```

# Роли пользователей
## Роль:	Возможности
**Аноним** Просмотр произведений, отзывов и комментариев
**Пользователь**	Создание отзывов/комментариев, оценка произведений
**Модератор**	Модерация всего контента (удаление/редактирование)
**Администратор**	Полный доступ + управление пользователями, категориями и жанрами
## Особенности
Уникальные отзывы - 1 пользователь = 1 отзыв на произведение
Динамический рейтинг - автоматический пересчет при новых оценках
Гибкая фильтрация - по категориям, жанрам, годам и рейтингу
Полная документация - с примерами запросов и ответов

## Технические характеристики:

- **Python**: 3.12
- **Django**: 5.1
- **Django REST Framework**: 3.15
- **JWT-аутентификация**: django-rest-framework-simplejwt 5.4
- **Утилиты**: PyJWT (2.10), Requests (2.32)

# Контакты
Разработано командой YaMDb:

## **Тимлид** Шаронов Игорь - Отзывы и рейтинги, рефакторинг кода
## Github: https://github.com/kocmoukurka/ 

## **Разработчик** Баранов Сергей - Произведения, Категории, Жанры
## Github: https://github.com/Zencat5888

## **Разработчик** Дудка Иван - Регистрация и аутентификация пользователей
## Github: https://github.com/stillin2it

Для более подробной информации посетите документацию API после запуска сервера.
