from django.contrib import admin
from .models import Book, Publisher, Author, Genre

admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Genre)