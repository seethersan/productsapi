import os

from django.core.exceptions import ValidationError

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

class Book(Model):
    class Meta:
        if 'read_capacity_units' in os.environ:
            read_capacity_units = int(os.environ['read_capacity_units'])
        else:
            read_capacity_units = 1
        if 'write_capacity_units' in os.environ:
            write_capacity_units = int(os.environ['write_capacity_units'])
        else: 
            write_capacity_units = 1
        table_name = "Book"
        if 'region' in os.environ:
            region = os.environ['region']
        else:
            host = "http://localhost:8787"
    id = UnicodeAttribute(hash_key=True)
    title = UnicodeAttribute(range_key=True)
    editorial = UnicodeAttribute()
    author = UnicodeAttribute()
    ISBN = UnicodeAttribute()
    genre = UnicodeAttribute()

    def validate_book(self):
        saved_book = [item.attribute_values for item in self.query(self.id)]
        errors = []
        if saved_book:
            errors.append(ValidationError("book", "{0} already exists".format(self.id)))
        if len(self.title) < 2 and len(self.title) > 75:
            errors.append(ValidationError("title", "Invalid book title"))
        if len(self.editorial) < 2 and len(self.editorial) > 55:
            errors.append(ValidationError("editorial", "Invalid editorial book"))
        if len(self.author) < 2 and len(self.author) > 55:
            errors.append(ValidationError("author", "Invalid book's author"))
        if len(self.ISNB) != 10 or len(self.ISBN) != 13:
            errors.append(ValidationError("ISBN", "Invalid book's ISBN "))
        if len(self.genre) < 2 and len(self.genre) > 40:
            errors.append(ValidationError("genre", "Invalid book's genre"))
        if errors:
            raise ValidationError(errors)

if not Book.exists():
    Book.create_table(wait=True)
