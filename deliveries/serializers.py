from rest_framework import serializers
from .models import Deliveries, ProductsInDeliveries


class ProductsInDeliveriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductsInDeliveries
        exclude = ('id', )


class DeliveriesSerializer(serializers.ModelSerializer):
    productsindeliveries_set = ProductsInDeliveriesSerializer()
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Deliveries
        fields = '__all__'
