from django.test import TestCase
from django.test import Client
from django.core.exceptions import ValidationError

from books.models import Book

# Create your tests here.
class BookTest(TestCase):


    def test_name_min_length(self):
        b = Book(id="1", title="en", editorial="Planeta", author="Jose", genre="Fantastico", ISBN="1234567890")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('title' in e.args[0][0].args[0])

    def test_name_max_length(self):
        b = Book(id="1", title="12345678901234567890123456789012345678901234567890123456", editorial="Planeta", author="Jose", genre="Fantastico", ISBN="1234567890")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('title' in e.args[0][0].args[0])
        
    def test_editorial_min_length(self):
        b = Book(id="1", title="La masa", editorial="Pl", author="Jose", genre="Fantastico", ISBN="1234567890")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('editorial' in e.args[0][0].args[0])

    def test_editorial_max_length(self):
        b = Book(id="1", title="La masa", editorial="12345678901234567890123456789012345678901234567890123456", author="Jose", genre="Fantastico", ISBN="1234567890")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('editorial' in e.args[0][0].args[0])

    def test_author_min_length(self):
        b = Book(id="1", title="La masa", editorial="Planeta", author="Jo", genre="Fantastico", ISBN="1234567890")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('author' in e.args[0][0].args[0])

    def test_author_max_length(self):
        b = Book(id="1", title="La masa", editorial="Planeta", author="12345678901234567890123456789012345678901234567890123456", genre="Fantastico", ISBN="1234567890")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('author' in e.args[0][0].args[0])

    def test_ISBN_length(self):
        b = Book(id="1", title="La masa", editorial="Planeta", author="Jose", genre="Fantastico", ISBN="123456789")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('ISBN' in e.args[0][0].args[0])

    def test_genre_min_length(self):
        b = Book(id="1", title="La masa", editorial="Planeta", author="Jose", genre="Fa", ISBN="1234567890")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('genre' in e.args[0][0].args[0])

    def test_genre_max_length(self):
        b = Book(id="1", title="La masa", editorial="Planeta", author="Jose", genre="12345678901234567890123456789012345678901234567890123456", ISBN="1234567890")
        try:
            b.validate_book()
        except ValidationError as e:
            self.assertTrue('genre' in e.args[0][0].args[0])