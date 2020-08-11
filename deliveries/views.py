from rest_framework import permissions, filters
from rest_framework import viewsets

from accounts.permissions import IsProvider
from .models import Deliveries
from .serializers import DeliveriesSerializer


class DeliveriesView(viewsets.ModelViewSet):
    """Эндпоинт на получение списка поставок и одного для поставщика
    Права доступа: авторизованный, пользователь в группе поставщиков
    Кладовщик может создавать, удалять и обновлять"""
    permission_classes = (permissions.IsAuthenticated, IsProvider)
    serializer_class = DeliveriesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['total_price', 'updated', 'created', 'status']
    search_fields = ['provider__provider_name', ]

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Deliveries.objects.all()
            return queryset
        else:
            queryset = Deliveries.objects.filter(provider__user=self.request.user.id)
            return queryset

    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy' or self.action == 'create':
            permissions_classes = (permissions.IsAdminUser,)
        elif self.request.user.is_staff:
            permissions_classes = (permissions.IsAdminUser,)
        else:
            permissions_classes = self.permission_classes
        return [permission() for permission in permissions_classes]
