import os

from django.core.exceptions import ValidationError

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute
)

# Create your models here.
class Product(Model):
    class Meta:
        if 'read_capacity_units' in os.environ:
            read_capacity_units = int(os.environ['read_capacity_units'])
        else:
            read_capacity_units = 1
        if 'write_capacity_units' in os.environ:
            write_capacity_units = int(os.environ['write_capacity_units'])
        else: 
            write_capacity_units = 1
        table_name = "Product"
        if 'region' in os.environ:
            region = os.environ['region']
        else:
            host = "http://localhost:8787"
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
    value = NumberAttribute(default=0)
    discount_value = NumberAttribute(default=0)
    stock = NumberAttribute(default=0)

    def validate_product(self):
        saved_product = [item.attribute_values for item in self.query(self.id)]
        errors = []
        if saved_product:
            errors.append(ValidationError("{0} already exists".format(self.id)))
        if len(self.name) < 2 and len(self.name) > 55:
            errors.append(ValidationError("name", "Invalid product name"))
        if self.stock < 0:
            errors.append(ValidationError("stock", "Invalid stock value"))
        if self.value <= 0 or self.value >= 99999.9:
            errors.append(ValidationError("value", "Invalid value"))
        if self.discount_value >= self.value:
            errors.append(ValidationError("discout_value", "Invalid discount_value"))
        if errors:
            raise Exception(errors)

if not Product.exists():
    Product.create_table(wait=True)