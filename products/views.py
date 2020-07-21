from rest_framework import viewsets

from .serializers import ProductSerializer, CategorySerializer

from .models import Product, Category

class ProductViewSet(viewsets.ModelViewSet):    
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer