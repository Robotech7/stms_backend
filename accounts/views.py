from django.contrib.auth.models import User
from rest_framework import permissions, serializers, status
from rest_framework.generics import (CreateAPIView,
                                     RetrieveAPIView,
                                     get_object_or_404,
                                     RetrieveUpdateAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProviderProfile
from .permissions import IsProvider
from .serializers import UserCreateSerializers, UserProfileSerializers, ProviderProfileSerializers, UserPasswordChangeSerializers


class UserCreateView(CreateAPIView):
    """Регистрация пользователя"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializers


class UserRetrieveView(RetrieveUpdateAPIView):
    """Профиль пользователя"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializers
    queryset = User.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, id=self.request.user.id)
        return obj


class ProviderProfileView(RetrieveAPIView):
    """Профиль поставщика"""
    permission_classes = (IsProvider,)
    serializer_class = ProviderProfileSerializers
    queryset = ProviderProfile.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, user=self.request.user.id)
        return obj

class UserPasswordChangeView(APIView):
    """Эндпоинт смены пароля"""
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request):
        """old_password --
           new_password --
           new_password_confirm --"""
        # Костыль, хз как сваггер подгонять, еще не разобрался
        obj = self.get_object()
        serializer = UserPasswordChangeSerializers(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if not self.request.user.check_password(data['old_password']):
                raise serializers.ValidationError({'old_password': 'Текущий пароль не верен'})
            if data['new_password'] != data['new_password_confirm']:
                raise serializers.ValidationError({'new_password': 'Пароли не совпадают'})
            obj.set_password(data['new_password'])
            obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


