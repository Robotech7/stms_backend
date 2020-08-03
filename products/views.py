from rest_framework import viewsets, permissions
from .models import Products, Categories
from .serializers import ProductsSerializer, CategorySerializer, CategoryProductsSerializer


class ProductsView(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт на получение всего списка продуктов и отдельного"""
    permission_classes = (permissions.AllowAny, )
    queryset = Products.objects.filter(is_active=True)
    serializer_class = ProductsSerializer


class CategoryView(viewsets.ReadOnlyModelViewSet):
    """Эндпоинт на получение списка категорий и товаров этой категории"""

    queryset = Categories.objects.filter(is_active=True).select_related()
    permission_classes = (permissions.AllowAny, )

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        elif self.action == 'retrieve':
            return CategoryProductsSerializer
