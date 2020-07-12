from django.test import TestCase
from django.test import Client
from django.core.validators import ValidationError

from products.models import Product
from products.views import Products

# Create your tests here.
class ProductTest(TestCase):

    def test_name_min_length(self):
        p = Product(id="product",name="pr",value=23,discount_value=2,stock=1)
        try:
            p.full_clean()
        except ValidationError as e:
            self.assertTrue('name' in e.message_dict)

    def test_name_max_length(self):
        p = Product(id="product",name="12345678901234567890123456789012345678901234567890123456",
                value=23,discount_value=2,stock=1)
        try:
            p.full_clean()
        except ValidationError as e:
            self.assertTrue('name' in e.message_dict)

    def test_value_min_value(self):
        p = Product(id="product",name="product",value=0,discount_value=2,stock=1)
        try:
            p.full_clean()
        except ValidationError as e:
            self.assertTrue('value' in e.message_dict)

    def test_value_max_value(self):
        p = Product(id="product",name="product",value=99999.9,discount_value=2,stock=1)
        try:
            p.full_clean()
        except ValidationError as e:
            self.assertTrue('value' in e.message_dict)

    def test_discount_value_man_value(self):
        p = Product(id="product",name="product",value=30,discount_value=30,stock=1)
        try:
            p.full_clean()
        except ValidationError as e:
            self.assertTrue('discount_value' in e.message_dict)

    def test_stock_min_value(self):
        p = Product(id="product",name="product",value=30,discount_value=3,stock=-1)
        try:
            p.full_clean()
        except ValidationError as e:
            self.assertTrue('stock' in e.message_dict)

class ProductView(TestCase):

    def test_product_get_response(self):
        c = Client()
        response = c.get('/api/products/')
        self.assertEqual(response.status_code, 200)