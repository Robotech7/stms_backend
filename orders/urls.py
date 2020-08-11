from django.urls import path

from .views import OrdersView, OrderVerifyView

urlpatterns = [
    path('', OrdersView.as_view({'get': 'list'})),
    path('create/', OrdersView.as_view({'post': 'create'})),
    path('delete/<int:pk>/', OrdersView.as_view({'delete': 'destroy'})),
    path('<int:pk>/', OrdersView.as_view({'get': 'retrieve'})),
    path('update/<int:pk>/', OrdersView.as_view({'put': 'update'})),
    path('verify/<int:pk>', OrderVerifyView.as_view(), name='verify_order')

]
