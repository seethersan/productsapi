from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from products.models import Product

import json

# Create your views here.
class Products(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return JsonResponse({"products": list(products.values())}, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class ProductsInsert(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        error_products = []
        new_products = []
        parse_errors = 0
        products = data.get("products")
        if products:
            for product in products:
                e = []
                try:
                    new_product = Product(**product)
                    new_product.full_clean()
                except ValidationError as errors:
                    for error in errors:
                        e.append(error[1][0])
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
                    "number_of_products_unable_to_parse": parse_errors
                }, safe=False)
            else:
                for new_product in new_products:
                    new_product.save()
                return JsonResponse(status=200, data={"status": "OK"})
        else:
            return JsonResponse(status=404, data={"error": "No products found"})