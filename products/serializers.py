from rest_framework import serializers
from .models import Product, Category, Brand

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    brands = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), many=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'value', 'discount_value', 'stock', 'categories', 'brands')
        extra_kwargs = {'categories': {'required': False}, 'brands': {'required': True}}

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'products')

class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = ('id', 'name', 'products')