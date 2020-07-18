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
        if 'write_capacity_units' in os.environ:
            write_capacity_units = int(os.environ['write_capacity_units'])
        table_name = "User"
        if 'region' in os.environ:
            region = os.environ['region']
        else:
            host = "http://localhost:8787"
    document_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
    profession = UnicodeAttribute()

    def validate_product(self):
        saved_user = [user.attribute_values for user in self.query(self.id)]
        errors = []
        if saved_user:
            errors.append(ValidationError("{0} already exists".format(self.id)))
        if len(self.document_id) < 8 and len(self.document_id) > 11:
            errors.append(ValidationError("name", "Invalid User document"))
        if len(self.name) < 2 and len(self.name) > 55:
            errors.append(ValidationError("name", "Invalid User name"))
        if len(self.profession) < 2 and len(self.profession) > 55:
            errors.append(ValidationError("name", "Invalid Profession"))
        if errors:
            raise Exception(errors)

if not User.exists():
    User.create_table(wait=True)