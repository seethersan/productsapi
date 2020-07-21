from rest_framework import viewsets

from .serializers import ProductSerializer, CategorySerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from products.models import Product, Category

import json

class ProductViewSet(viewsets.ModelViewSet):    
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer