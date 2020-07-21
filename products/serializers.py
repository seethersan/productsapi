from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'value', 'discount_value', 'stock', 'categories')
        extra_kwargs = {'categories': {'required': False}}