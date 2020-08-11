from rest_framework import viewsets, permissions, filters

from .models import Products, Categories
from .serializers import ProductsSerializer, CategorySerializer, CategoryProductsSerializer


class ProductsView(viewsets.ModelViewSet):
    """Эндпоинт на получение всего списка продуктов и отдельного
    Только кладовщик может удалять, создавать, обновлять"""
    permission_classes = (permissions.AllowAny,)
    queryset = Products.objects.filter(is_active=True)
    serializer_class = ProductsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['price', 'in_storage']
    search_fields = ['name', 'category', 'bar_code']

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Products.objects.all()
        else:
            queryset = self.queryset
        return queryset

    def get_permissions(self):
        print(self.action)
        if self.action == 'update' or self.action == 'destroy' or self.action == 'create':
            permissions_classes = (permissions.IsAdminUser,)
        else:
            permissions_classes = self.permission_classes
        return [permission() for permission in permissions_classes]


class CategoryView(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт на получение списка категорий и товаров этой категории"""

    queryset = Categories.objects.filter(is_active=True).select_related()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        elif self.action == 'retrieve':
            return CategoryProductsSerializer
