import os

from django.core.exceptions import ValidationError

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

class User(Model):
    class Meta:
        if 'read_capacity_units' in os.environ:
            read_capacity_units = int(os.environ['read_capacity_units'])
        else:
            read_capacity_units = 1
        if 'write_capacity_units' in os.environ:
            write_capacity_units = int(os.environ['write_capacity_units'])
        else: 
            write_capacity_units = 1
        table_name = "User"
        if 'region' in os.environ:
            region = os.environ['region']
        else:
            host = "http://localhost:8787"
    document_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
    profession = UnicodeAttribute()

    def validate_user(self):
        saved_user = [user.attribute_values for user in self.query(self.document_id)]
        errors = []
        if saved_user:
            errors.append(ValidationError("{0} already exists".format(self.document_id)))
        if len(self.document_id) < 8 and len(self.document_id) > 11:
            errors.append(ValidationError("document_id", "Invalid User document_id"))
        if len(self.name) < 2 and len(self.name) > 55:
            errors.append(ValidationError("name", "Invalid User name"))
        if len(self.profession) < 2 and len(self.profession) > 55:
            errors.append(ValidationError("profession", "Invalid User profession"))
        if errors:
            raise ValidationError(errors)

if not User.exists():
    User.create_table(wait=True)