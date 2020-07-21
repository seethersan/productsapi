from rest_framework import viewsets

from .serializers import ProductSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from products.models import Product

import json


@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):    
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer