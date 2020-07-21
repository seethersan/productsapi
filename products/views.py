from rest_framework import viewsets

from .serializers import ProductSerializer, CategorySerializer, BrandSerializer

from .models import Product, Category, Brand

class ProductViewSet(viewsets.ModelViewSet):    
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer