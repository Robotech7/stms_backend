from rest_framework import permissions
from rest_framework import viewsets

from accounts.permissions import IsProvider
from .models import Deliveries
from .serializers import DeliveriesSerializer


class DeliveriesView(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт на получение списка поставок и одного
    Права доступа: авторизованный, пользователь в группе поставщиков"""
    permission_classes = (permissions.IsAuthenticated, IsProvider)
    serializer_class = DeliveriesSerializer

    def get_queryset(self):
        queryset = Deliveries.objects.filter(provider__user=self.request.user.id)
        return queryset
