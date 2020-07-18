from django.test import TestCase
from django.test import Client
from django.core.validators import ValidationError

from products.models import Product
from products.views import Products, ProductsInsert

import json

class ProductTest(TestCase):

    def test_name_min_length(self):
        p = Product(id="product23",name="pr",value=23,discount_value=2,stock=1)
        try:
            p.validate_product()
        except Exception as e:
            self.assertTrue(ValidationError(['name']) in e.args[0][0].args[0])

    def test_name_max_length(self):
        p = Product(id="product43",name="12345678901234567890123456789012345678901234567890123456",
                value=23,discount_value=2,stock=1)
        try:
            p.validate_product()
        except Exception as e:
            self.assertTrue('name' in e.args[0][0].args[0])

    def test_value_min_value(self):
        p = Product(id="product12",name="product",value=0,discount_value=2,stock=1)
        try:
            p.validate_product()
        except Exception as e:
            self.assertTrue('value' in e.args[0][0].args[0])

    def test_value_max_value(self):
        p = Product(id="product45",name="product",value=99999.9,discount_value=2,stock=1)
        try:
            p.validate_product()
        except Exception as e:
            self.assertTrue('value' in e.args[0][0].args[0])

    def test_discount_value_max(self):
        p = Product(id="product34",name="product",value=30,discount_value=30,stock=1)
        try:
            p.validate_product()
        except Exception as e:
            self.assertEquals('discount_value', e.args[0][0].args[0])

    def test_stock_min_value(self):
        p = Product(id="product90",name="product",value=30,discount_value=3,stock=-1)
        try:
            p.validate_product()
        except Exception as e:
            self.assertTrue('stock' in e.args[0][0].args[0])

