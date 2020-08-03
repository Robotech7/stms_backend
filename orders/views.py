from rest_framework import viewsets, permissions

from .models import Orders
from .serializers import OrdersSerializer


class OrdersView(viewsets.ModelViewSet):
    """Вьюсет для заказов, на создание, чтение и удаление"""
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = OrdersSerializer

    def get_queryset(self):
        if self.request.user:
            queryset = Orders.objects.filter(user__id=self.request.user.id)
            return queryset

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
