from django.contrib import admin

from reviews.models import Category, Comment, Genre, Title, Review

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
