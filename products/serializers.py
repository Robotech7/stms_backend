from rest_framework import serializers
from .models import Products, Categories, ProductsImage


class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        fields = ['image', ]


class ProductsSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField('name', read_only=True)
    products_images = ProductsImageSerializer(many=True)

    class Meta:
        model = Products
        exclude = ('created', 'updated', 'is_active')


class CategoryProductsSerializer(serializers.ModelSerializer):
    products_set = ProductsSerializer(many=True)

    class Meta:
        model = Categories
        fields = ['id', 'name', 'products_set']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'name')
