from rest_framework import serializers
from .models import Publisher, Author, Genre, Book

class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'name')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class BookSerializer(serializers.HyperlinkedModelSerializer):
    publishers = PublisherSerializer(many=True, read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'ISBN', 'publishers', 'authors', 'genres')
        extra_kwargs = {'publishers': {'required': True}, 'authors': {'required': True}, 'genres': {'required': False}}