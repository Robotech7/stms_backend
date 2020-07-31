from django.urls import path
from .views import ProductsView, CategoryView


urlpatterns = [
    path('', ProductsView.as_view({'get': 'list'})),
    path('<int:pk>', ProductsView.as_view({'get': 'retrieve'})),
    path('category/', CategoryView.as_view({'get': 'list'})),
    path('category/<int:pk>', CategoryView.as_view({'get': 'retrieve'})),

]
