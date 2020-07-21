from rest_framework import serializers
from .models import Publisher, Author, Genre, Book

class BookSerializer(serializers.ModelSerializer):
    publishers = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all(), many=True)
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    
    class Meta:
        model = Book
        fields = ('id', 'title', 'ISBN', 'publishers', 'authors', 'genres')
        extra_kwargs = {'publishers': {'required': True}, 'authors': {'required': True}, 'genres': {'required': False}}

class PublisherSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Publisher
        fields = ('id', 'name', 'books')

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'books')

class GenreSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ('id', 'name', 'books')