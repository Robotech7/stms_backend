from django.urls import path

from .views import UserCreateView, UserRetrieveView, ProviderProfileView, UserPasswordChangeView

urlpatterns = [
    path('register/', UserCreateView.as_view()),
    path('profile/', UserRetrieveView.as_view()),
    path('provider_profile/', ProviderProfileView.as_view()),
    path('change_password/', UserPasswordChangeView.as_view()),
]
