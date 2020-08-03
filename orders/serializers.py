from rest_framework import serializers
from .models import Orders, ProductsInOrder
from products.models import Products


class ProductsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ('name', 'id')


class ProductsInOrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductsInOrder
        exclude = ('order', 'id')
        read_only_fields = ('price_for_one', 'order')


class OrdersSerializer(serializers.ModelSerializer):
    productsinorder_set = ProductsInOrderSerializers(many=True)
    status = serializers.CharField(source='get_status_display', read_only=True)

    def create(self, validated_data):
        products_in_order = validated_data.pop('productsinorder_set')
        order = Orders.objects.create(**validated_data)
        for product in products_in_order:
            ProductsInOrder.objects.create(**product, order=order)
        return order

    class Meta:
        model = Orders
        exclude = ('user', )
        read_only_fields = ('total_price', )
