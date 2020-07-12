from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from products.models import Product

# Create your views here.
class Products(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return JsonResponse({"products": list(products.values())}, safe=False)