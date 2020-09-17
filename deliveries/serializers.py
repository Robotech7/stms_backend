from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Deliveries, ProductsInDeliveries


class ProductsInDeliveriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductsInDeliveries
        fields = ('id', 'amount', 'product')


class DeliveriesSerializer(WritableNestedModelSerializer):
    productsindeliveries_set = ProductsInDeliveriesSerializer(many=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    # def create(self, validated_data):
    #     products_in_delivery = validated_data.pop('productsindeliveries_set')
    #     delivery = Deliveries.objects.create(**validated_data)
    #     for product in products_in_delivery:
    #         ProductsInDeliveries.objects.create(**product, delivery=delivery)
    #     return delivery
    #
    # def update(self, instance, validated_data):
    #     instance.provider = validated_data.get('provider', instance.provider)
    #     instance.total_price = validated_data.get('total_price', instance.total_price)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.save()
    #     products = validated_data.get('productsindeliveries_set')
    #     print(products)
    #     if products is not None:
    #         for product in products:
    #             product_id = product.get('id', None)
    #             if product_id:
    #                 product_item = ProductsInDeliveries.objects.get(id=product_id, delivery=instance)
    #                 product_item.amount = product.get('amount', product.amount)
    #                 product_item.save()
    #             else:
    #                 ProductsInDeliveries.objects.create(delivery=instance, **product)
    #     return instance

    class Meta:
        model = Deliveries
        fields = '__all__'
