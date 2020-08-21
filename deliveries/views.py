from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from accounts.permissions import IsProvider
from .models import Deliveries
from .serializers import DeliveriesSerializer


class DeliveriesView(viewsets.ModelViewSet):
    """Эндпоинт на получение списка поставок и одного для поставщика
    Права доступа: авторизованный, пользователь в группе поставщиков
    Кладовщик может создавать, удалять и обновлять"""
    permission_classes = (permissions.IsAuthenticated, IsProvider)
    serializer_class = DeliveriesSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['total_price', 'updated', 'created', 'status']
    search_fields = ['provider__provider_name', ]

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Deliveries.objects.all()
        else:
            queryset = Deliveries.objects.prefetch_related('productsindeliveries_set') \
                .filter(provider__user=self.request.user.id)
        return queryset

    def get_permissions(self):
        if self.action == any(['update', 'create', 'destroy']):
            permissions_classes = (permissions.IsAdminUser,)
        elif self.request.user.is_staff:
            permissions_classes = (permissions.IsAdminUser,)
        else:
            permissions_classes = self.permission_classes
        return [permission() for permission in permissions_classes]
