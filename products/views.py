from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Products, Categories
from .serializers import ProductsSerializer, CategorySerializer, CategoryProductsSerializer


class ProductsView(viewsets.ModelViewSet):
    """Эндпоинт на получение всего списка продуктов и отдельного
    Только кладовщик может удалять, создавать, обновлять"""
    permission_classes = (permissions.AllowAny,)
    queryset = Products.objects.filter(is_active=True)
    serializer_class = ProductsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['price', 'in_storage']
    search_fields = ['name', 'category__name', 'bar_code']

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Products.objects.all()
        else:
            queryset = self.queryset
        return queryset

    def get_permissions(self):
        if self.action == any(['update', 'create', 'destroy']):
            permissions_classes = (permissions.IsAdminUser,)
        else:
            permissions_classes = self.permission_classes
        return [permission() for permission in permissions_classes]


class CategoryView(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт на получение списка категорий и товаров этой категории"""

    queryset = Categories.objects.filter(is_active=True).prefetch_related('products_set')
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        elif self.action == 'retrieve':
            return CategoryProductsSerializer
