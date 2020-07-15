from django.test import TestCase
from django.test import Client
from django.core.validators import ValidationError

from products.models import Product
from products.views import Products, ProductsInsert

import json

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

    def test_product_get_content(self):
        c = Client()
        products = [
            	{
                    "id": "product",
                    "name": "awesome product",
                    "value": 29.3,
                    "discount_value": 3.2,
                    "stock": 3
                },
                {
                    "id": "product1",
                    "name": "awesome product1",
                    "value": 291.3,
                    "discount_value": 33.2,
                    "stock": 3
                }
        ]
        create = c.post('/api/products/bulk_insert', json.dumps({'products': products}),
                        content_type="application/json")
        response = c.get('/api/products/')
        response_products = json.loads(response.content)
        self.assertEqual(products, response_products["products"])

    def test_product_post_success_response(self):
        c = Client()
        data = {
            "id": "product2",
            "name": "awesome product2",
            "value": 29.3,
            "discount_value": 3.2,
            "stock": 3
        }
        response = c.post('/api/products/', json.dumps(data),
                        content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_product_post_fail_response(self):
        c = Client()
        data = {
            "id": "product2",
            "name": "awesome product2",
            "value": 29.3,
            "discount_value": 32.2,
            "stock": -3
        }
        response = c.post('/api/products/', json.dumps(data),
                        content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_product_post_fail_validators(self):
        c = Client()
        data = {
            "id": "productm",
            "name": "aw",
            "value": 0,
            "discount_value": 32.2,
            "stock": -3
        }
        response = c.post('/api/products/', json.dumps(data),
                        content_type="application/json")
        errors = json.loads(response.content)["errors"]
        self.assertTrue("Invalid product name" in errors)
        self.assertTrue("Invalid value" in errors)
        self.assertTrue("Invalid discount value" in errors)
        self.assertTrue("Invalid stock value" in errors)

    def test_bulk_insert_post_success_response(self):
        c = Client()
        products = [
            	{
                    "id": "product3",
                    "name": "awesome product",
                    "value": 29.3,
                    "discount_value": 3.2,
                    "stock": 3
                },
                {
                    "id": "product4",
                    "name": "awesome product2",
                    "value": 291.3,
                    "discount_value": 33.2,
                    "stock": 3
                }
        ]
        response = c.post('/api/products/bulk_insert', json.dumps({'products': products}),
                        content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_bulk_insert_post_fail_response(self):
        c = Client()
        products = [
            	{
                    "id": "product5",
                    "name": "aw",
                    "value": 29.3,
                    "discount_value": 3.2,
                    "stock": -3
                },
                {
                    "id": "product6",
                    "name": "awesome product2",
                    "value": 291.3,
                    "discount_value": 333.2,
                    "stock": 3
                }
        ]
        response = c.post('/api/products/bulk_insert', json.dumps({'products': products}),
                    content_type="application/json")
        self.assertEqual(response.status_code, 422)

    def test_bulk_insert_post_fail_validators(self):
        c = Client()
        products = [
            	{
                    "id": "product7",
                    "name": "aw",
                    "value": 0,
                    "discount_value": 32.2,
                    "stock": -3
                }
        ]
        response = c.post('/api/products/bulk_insert', json.dumps({'products': products}),
                    content_type="application/json")
        errors = json.loads(response.content)["products_report"][0]["errors"]
        self.assertTrue("Invalid product name" in errors)
        self.assertTrue("Invalid value" in errors)
        self.assertTrue("Invalid discount value" in errors)
        self.assertTrue("Invalid stock value" in errors)

    def test_bulk_insert_post_fail_parse(self):
        c = Client()
        products = [
            	{
                    "ide": "product"
                },
                {
                    "names": "products"
                },
                {
                    "values": "323"
                },
                {
                    "id": "product",
                    "name": "awesome product",
                    "value": "asf",
                    "discount_value": 32.2,
                    "stock": -3
                }
        ]
        response = c.post('/api/products/bulk_insert', json.dumps({'products': products}),
                    content_type="application/json")
        error = json.loads(response.content)
        self.assertEqual(4, error["number_of_products_unable_to_parse"])