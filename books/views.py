from rest_framework import viewsets

from .serializers import PublisherSerializer, AuthorSerializer, GenreSerializer, BookSerializer

from .models import Publisher, Author, Genre, Book

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all().order_by('id')
    serializer_class = PublisherSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
