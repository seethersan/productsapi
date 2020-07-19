from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from products.models import Product

import json

@method_decorator(csrf_exempt, name='dispatch')
class Products(View):
    def get(self, request, *args, **kwargs):
        products = [item.attribute_values for item in Product.scan()]
        return JsonResponse({"products": products}, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        e = []
        try:
            new_product = Product(**data)
            new_product.validate_product()
        except Exception as errors:
            for error in errors.args[0]:
                e.append(error.args[0])
            return JsonResponse(status=422, data={
                "status": "ERROR",
                "product_id": data['id'],
                "errors": e
            }, safe=False)
        else:
            new_product.save()
            return JsonResponse(status=200, data={"status": "OK"})

@method_decorator(csrf_exempt, name='dispatch')
class ProductsInsert(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        error_products = []
        new_products = []
        parse_errors = 0
        products = data.get("products")
        if products:
            with Product.batch_write() as batch:
                for product in products:
                    e = []
                    try:
                        new_product = Product(**product)
                        new_product.validate_product()
                    except ValidationError as errors:
                        for error in errors.args[0]:
                            e.append(error.args[1])
                        error_products.append({
                            "product_id": new_product.id,
                            "errors": e
                        })
                    except Exception:
                        parse_errors += 1
                    else:
                        new_products.append(new_product)
                if error_products or parse_errors:
                    return JsonResponse(status=422, data={
                        "status": "ERROR",
                        "products_report": error_products,
                        "number_of_books_unable_to_parse": parse_errors
                    }, safe=False)
                else:
                    for new_product in new_products:
                        batch.save(new_product)
                    return JsonResponse(status=200, data={"status": "OK"})