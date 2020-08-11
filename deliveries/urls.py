from django.urls import path

from .views import DeliveriesView

urlpatterns = [
    path('<int:pk>/', DeliveriesView.as_view({'get': 'retrieve'})),
    path('', DeliveriesView.as_view({'get': 'list'})),
    path('create/', DeliveriesView.as_view({'post': 'create'})),
    path('update/<int:pk>', DeliveriesView.as_view({'put': 'update'})),
    path('delete/<int:pk>', DeliveriesView.as_view({'delete': 'destroy'})),
]
