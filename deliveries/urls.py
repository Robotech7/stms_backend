from django.urls import path

from .views import DeliveriesView

urlpatterns = [
    path('<int:pk>/', DeliveriesView.as_view({'get': 'retrieve'})),
    path('', DeliveriesView.as_view({'get': 'list'}))
]
