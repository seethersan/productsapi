from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, ValidationError

class Publisher(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3, "Invalid publisher name"), MaxLengthValidator(55, "Invalid publisher name")])

    def __str__(self):
        return self.name

class Author(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(3, "Invalid author first name"), MaxLengthValidator(50, "Invalid author first name")])
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(3, "Invalid author last name"), MaxLengthValidator(50, "Invalid author last name")])

    def __str__(self):
        return self.first_name + " " + self.last_name

class Genre(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3, "Invalid genre name"), MaxLengthValidator(55, "Invalid genre name")])

    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=70, validators=[MinLengthValidator(3, "Invalid book title"), MaxLengthValidator(70, "Invalid book title")])
    ISBN = models.CharField(max_length=13, validators=[MinLengthValidator(10, "Invalid ISBN"), MaxLengthValidator(13, "Invalid ISBN")])
    publishers = models.ManyToManyField(Publisher)
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title