from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from products.models import Products
from .models import Orders, ProductsInOrder, QrCodesOrderVerify


class QrCodesOrderVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCodesOrderVerify
        fields = ('qr',)


class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('name', 'id')


class ProductsInOrderSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductsInOrder
        exclude = ('order',)
        read_only_fields = ('price_for_one', 'order')


class OrdersSerializer(WritableNestedModelSerializer):
    productsinorder_set = ProductsInOrderSerializers(many=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    qrcodesorderverify = QrCodesOrderVerifySerializer()

    def to_representation(self, instance):
        # Метод для вывода QR только админу(кладовщику)
        representation = super().to_representation(instance)
        qr = representation.pop('qrcodesorderverify', '')
        if self.context['request'].user.is_staff:
            representation['qr_codes'] = qr
        return representation

    # def create(self, validated_data):
    #     products_in_order = validated_data.pop('productsinorder_set')
    #     order = Orders.objects.create(**validated_data)
    #     for product in products_in_order:
    #         ProductsInOrder.objects.create(**product, order=order)
    #     return order
    #
    # def update(self, instance, validated_data):
    #     instance.client_phone = validated_data.get('client_phone', instance.client_phone)
    #     instance.client_name = validated_data.get('client_name', instance.client_name)
    #     instance.client_surname = validated_data.get('client_surname', instance.client_surname)
    #     instance.client_email = validated_data.get('client_email', instance.client_email)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.save()
    #
    #     products = validated_data.get('productsinorder_set')
    #     if products is not None:
    #         for product in products:
    #             product_id = product.get('id', None)
    #             if product_id:
    #                 product_item = ProductsInOrder.objects.get(id=product_id, order=instance)
    #                 product_item.amount = product.get('amount', product_item.amount)
    #                 product_item.save()
    #             else:
    #                 new_product = ProductsInOrder(order=instance, **product)
    #                 new_product.save()
    #     return instance

    class Meta:
        model = Orders
        fields = '__all__'
        read_only_fields = ('total_price',)
