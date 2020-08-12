from rest_framework import serializers

from .models import Products, Categories, ProductsImage


class ProductsImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductsImage
        fields = ['image', 'id']


class ProductsSerializer(serializers.ModelSerializer):
    productsimage_set = ProductsImageSerializer(many=True)
    category = serializers.SlugRelatedField(slug_field='name', queryset=Categories.objects.all())

    def create(self, validated_data):
        products_image = validated_data.pop('productsimage_set')
        product = Products.objects.create(**validated_data)
        for image in products_image:
            ProductsImage.objects.create(product=product, **image)
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.in_storage = validated_data.get('in_storage', instance.in_storage)
        instance.bar_code = validated_data.get('bar_code', instance.bar_code)
        instance.save()
        product_images = validated_data.pop('productsimage_set')
        for image in product_images:
            image_id = image.get('id', None)
            if image_id:
                product_image = ProductsImage.objects.get(id=image_id)
                product_image.image = image.get('image', product_image.image)
                product_image.save()
            else:
                ProductsImage.objects.create(product=instance, **image)
        return instance

    class Meta:
        model = Products
        exclude = ('is_active',)


class CategoryProductsSerializer(serializers.ModelSerializer):
    products_set = ProductsSerializer(many=True)

    class Meta:
        model = Categories
        fields = ['id', 'name', 'products_set']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'name')
