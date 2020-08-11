from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Orders
from .serializers import OrdersSerializer


class OrdersView(viewsets.ModelViewSet):
    """Вьюсет для заказов, на создание, чтение и удаление.
    Заказы только авторизованного пользователя
    Администратор(кладовщик) видит все
    Обновлять может только кладовщик"""
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = OrdersSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['total_price', 'status', 'updated']
    search_fields = ['client_name', 'client_email', 'user__username']

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Orders.objects.all()
            return queryset
        else:
            queryset = Orders.objects.filter(user__id=self.request.user.id)
            return queryset

    def perform_destroy(self, instance):
        instance.delete()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'update':
            permissions_classes = (permissions.IsAdminUser,)
        else:
            permissions_classes = self.permission_classes
        return [permission() for permission in permissions_classes]


class OrderVerifyView(APIView):
    """Подтверждение заказа по QR, только авторизованный пользователь и его заказ"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        queryset = Orders.objects.filter(user=request.user.id, status=3)
        if queryset.exists():
            obj = get_object_or_404(queryset, id=pk)
            obj.status = 4
            obj.save()
            serializer = OrdersSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'errors': 'Видимо это не ваш заказ'}, status=status.HTTP_400_BAD_REQUEST)
